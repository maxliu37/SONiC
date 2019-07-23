#include <assert.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/limits.h>

#define MAX_NUM_TARGETS 5
#define MAX_NUM_UNITS 128

static const char* UNIT_FILE_PREFIX = "/etc/systemd/system/";
static const char* CONFIG_FILE = "/etc/sonic/generated_services.conf";


void strip_trailing_newline(char* str) {
    /***
    Strips trailing newline from a string if it exists
    ***/

    size_t l = strlen(str);
    if (l > 0 && str[l-1] == '\n')
        str[l-1] = '\0';
}


static int get_target_lines(char* unit_file, char* target_lines[]) {
    /***
    Gets installation information for a given unit file

    Returns lines in the [Install] section of a unit file
    ***/
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    bool found_install;
    int num_target_lines;


    fp = fopen(unit_file, "r");

    if (fp == NULL) {
        exit(EXIT_FAILURE);
    }

    found_install = false;
    num_target_lines = 0;

    while ((read = getline(&line, &len, fp)) != -1 ) {
        // Assumes that [Install] is the last section of the unit file
        if (strstr(line, "[Install]") != NULL) {
             found_install = true;
        }
        else if (found_install) {
            target_lines[num_target_lines] = strdup(line);
            num_target_lines++;
        }
    }

    free(line);

    fclose(fp);

    return num_target_lines;
}

static int get_install_targets_from_line(char* target_string, char* suffix, char* targets[]) {
    /***
    Helper fuction for get_install_targets

    Given a space delimited string of target directories and a suffix,
    puts each target directory plus the suffix into the targets array
    ***/
    char* token;
    char* target;
    char final_target[PATH_MAX];
    int num_targets = 0;

    while ((token = strtok_r(target_string, " ", &target_string))) {
        target = strdup(token);
        strip_trailing_newline(target);

        strcpy(final_target, target);
        strcat(final_target, suffix);

        free(target);

        targets[num_targets] = strdup(final_target);
        num_targets++;
    }
    return num_targets;
}

static int get_install_targets(char* unit_file, char* targets[]) {
    /***
    Returns install targets for a unit file

    Parses the information in the [Install] section of a given
    unit file to determine which directories to install the unit in
    ***/
    char file_path[PATH_MAX];
    char *target_lines[5];
    int num_target_lines;
    int num_targets;
    char* token;
    char* line = NULL;
    bool first;
    char* target_suffix;

    strcpy(file_path, UNIT_FILE_PREFIX);
    strcat(file_path, unit_file);

    num_target_lines = get_target_lines(file_path, target_lines);

    num_targets = 0;

    for (int i = 0; i < num_target_lines; i++) {
        line = target_lines[i];
        first = true;

        while ((token = strtok_r(line, "=", &line))) {
            if (first) {
                first = false;

                if (strstr(token, "RequiredBy") != NULL) {
                    target_suffix = ".requires";
                }
                else if (strstr(token, "WantedBy") != NULL) {
                    target_suffix = ".wants";
                }
            }
            else {
                num_targets += get_install_targets_from_line(token, target_suffix, &targets[num_targets]);
            }
        }
        free(target_lines[i]);
    }
    return num_targets;
}


static int get_unit_files(char* unit_files[]){
    /***
    Reads a list of unit files to be installed from /etc/sonic/generated_services.conf
    ***/
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen(CONFIG_FILE, "r");

    if (fp == NULL) {
        exit(EXIT_FAILURE);
    }

    int num_unit_files = 0;

    while ((read = getline(&line, &len, fp)) != -1) {
        strip_trailing_newline(line);
        unit_files[num_unit_files] = strdup(line);
        num_unit_files++;
    }

    free(line);

    fclose(fp);

    return num_unit_files;

}


static int install_unit_file(char* unit_file, char* target, char* install_dir) {
    /***
    Creates a symlink for a unit file installation

    For a given unit file and target directory,
    create the appropriate symlink in the target directory
    to enable the unit and have it started by Systemd
    ***/
    char final_install_dir[PATH_MAX];
    char src_path[PATH_MAX];
    char dest_path[PATH_MAX];
    struct stat st;
    int r;

    assert(unit_file);
    assert(target);

    strcpy(final_install_dir, install_dir);
    strcat(final_install_dir, target);

    strcpy(src_path, UNIT_FILE_PREFIX);
    strcat(src_path, unit_file);

    if (stat(final_install_dir, &st) == -1) {
        // If doesn't exist, create
        mkdir(final_install_dir, 0755);
    }
    else if (S_ISREG(st.st_mode)) {
        // If is regular file, remove and create
        remove(final_install_dir);
        mkdir(final_install_dir, 0755);
    }  
    else if (S_ISDIR(st.st_mode)) {
        // If directory, verify correct permissions
        chmod(final_install_dir, 0755);
    }
        

    strcpy(dest_path, final_install_dir);
    strcat(dest_path, "/");
    strcat(dest_path, unit_file);

    r = symlink(src_path, dest_path);

    if (r < 0) {
        if (errno == EEXIST)
            return 0;

        return 1;
    }

    return 0;

}


int main(int argc, char **argv) {
    char* unit_files[MAX_NUM_UNITS];
    char install_dir[PATH_MAX];
    char* targets[MAX_NUM_TARGETS];
    int num_unit_files;
    int num_targets;

    if (argc <= 1) {
        fputs("Installation directory required as argument\n", stderr);
        return 1;
    }

    strcpy(install_dir, argv[1]);
    strcat(install_dir, "/");

    num_unit_files = get_unit_files(unit_files);

    // For each unit file, get the installation targets and install the unit
    for (int i = 0; i < num_unit_files; i++) {
        num_targets = get_install_targets(unit_files[i], targets);
        for(int j = 0; j < num_targets; j++) {
            if (install_unit_file(unit_files[i], targets[j], install_dir) != 0) {
                return 1;
            }
            free(targets[j]);
        }

        free(unit_files[i]);
    }
    return 0;
}
