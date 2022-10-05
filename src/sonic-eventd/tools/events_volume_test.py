import sys
import subprocess
import time
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers = [
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def read_events_from_file(file, count):
    logging.info("Reading from file generated by events_tool")
    lines = 0
    with open(file, 'r') as infile:
        lines = infile.readlines()
    logging.info("Should receive {} events and got {} events\n".format(count, len(lines)))
    assert len(lines) == count

def start_tool(file):
    logging.info("Starting events_tool\n")
    proc = subprocess.Popen(["./events_tool", "-r", "-o", file])
    return proc

def run_test(process, file, count, duplicate):
    # log messages to see if events have been received
    tool_proc = start_tool(file)

    time.sleep(2) # buffer for events_tool to startup 
    logging.info("Generating logger messages\n")
    for i in range(count):
        line = ""
        state = "up"
        if duplicate:
            line = "{} test message testmessage state up".format(process)
        else:
            if i % 2 != 1:
                state = "down"
            line = "{} test message testmessage{} state {}".format(process, i, state)
        command = "logger -p local0.notice -t {}".format(line)
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    time.sleep(2) # some buffer for all events to be published to file
    read_events_from_file(file, count)
    tool_proc.terminate()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--process", nargs='?', const ='', default='', help="Process that is spitting out log")
    parser.add_argument("-f", "--file", nargs='?', const='', default='', help="File used by events_tool to read events from")
    parser.add_argument("-c", "--count", type=int, nargs='?', const=1000, default=1000, help="Count of times log message needs to be published down/up, default is 1000")
    args = parser.parse_args()
    if(args.process == '' or args.file == ''):
        logging.error("Invalid process or logfile\n")
        return
    logging.info("Starting volume test\n")
    logging.info("Generating {} unique messages for rsyslog plugin\n".format(args.count))
    run_test(args.process, args.file, args.count, False)
    time.sleep(2)
    logging.info("Restarting volume test but for duplicate log messages\n")
    run_test(args.process, args.file, args.count, True)

if __name__ == "__main__":
    main()
