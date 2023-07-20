#!/usr/bin/env python
# @Company ：Celestica
# @Time    : 2023/2/28 plugins:10
# @Mail    : yajiang@celestica.com
# @Author  : jiang tao
import os
import struct
import subprocess
from sonic_py_common import device_info
from mmap import *

HOST_CHK_CMD = "docker > /dev/null 2>&1"
EMPTY_STRING = ""


class APIHelper(object):

    def __init__(self):
        (self.platform, self.hwsku) = device_info.get_platform_and_hwsku()

    @staticmethod
    def is_host():
        return os.system(HOST_CHK_CMD) == 0

    @staticmethod
    def pci_get_value(resource, offset):
        status = True
        result = ""
        try:
            fd = os.open(resource, os.O_RDWR)
            mm = mmap(fd, 0)
            mm.seek(int(offset))
            read_data_stream = mm.read(4)
            result = struct.unpack('I', read_data_stream)
        except Exception:
            status = False
        return status, result

    @staticmethod
    def run_command(cmd):
        status = True
        result = ""
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            if err.decode("utf-8") == "":
                result = raw_data.decode("utf-8").strip()
        except Exception:
            status = False
        return status, result

    @staticmethod
    def run_interactive_command(cmd):
        try:
            os.system(cmd)
        except Exception:
            return False
        return True

    @staticmethod
    def read_txt_file(file_path):
        try:
            with open(file_path, 'r') as fd:
                data = fd.read()
                return data.strip()
        except IOError:
            pass
        return None

    @staticmethod
    def read_one_line_file(file_path):
        try:
            with open(file_path, 'r') as fd:
                data = fd.readline()
                return data.strip()
        except IOError:
            pass
        return None

    @staticmethod
    def write_txt_file(file_path, value):
        try:
            with open(file_path, 'w') as fd:
                fd.write(str(value))
        except Exception as E:
            print(str(E))
            return False
        return True

    def get_cpld_reg_value(self, getreg_path, register):
        cmd = "echo {1} > {0}; cat {0}".format(getreg_path, register)
        status, result = self.run_command(cmd)
        return result if status else None

    @staticmethod
    def ipmi_raw(cmd):
        status = True
        result = ""
        try:
            cmd = "ipmitool raw {}".format(str(cmd))
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            if err.decode("utf-8") == "":
                result = raw_data.decode("utf-8").strip()
            else:
                status = False
        except Exception:
            status = False
        return status, result

    @staticmethod
    def ipmi_fru_id(key_id, key=None):
        status = True
        result = ""
        try:
            cmd = "ipmitool fru print {}".format(str(
                key_id)) if not key else "ipmitool fru print {0} | grep '{1}' ".format(str(key_id), str(key))

            p = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            if err == '':
                result = raw_data.strip()
            else:
                status = False
        except Exception:
            status = False
        return status, result

    @staticmethod
    def ipmi_set_ss_thres(id, threshold_key, value):
        status = True
        result = ""
        try:
            cmd = "ipmitool sensor thresh '{}' {} {}".format(
                str(id), str(threshold_key), str(value))
            p = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            if err == '':
                result = raw_data.strip()
            else:
                status = False
        except Exception:
            status = False
        return status, result