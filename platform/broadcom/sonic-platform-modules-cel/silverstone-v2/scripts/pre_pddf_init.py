#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2023/7/24 9:34
# @Mail    : yajiang@celestica.com
# @Author  : jiang tao
# @Function: Load pddf_custom_lpc_basecpld.ko, after confirming the BMC is in place,
#            load different configuration files, and finally remove the driver.

import subprocess
import os


class PrePddfInit(object):
    def __init__(self):
        self.ker_path = "/usr/lib/modules/{}/extra"
        self.lpc_basecpld_name = "pddf_custom_lpc_basecpld"
        self.lpc_basecpld_ko = "pddf_custom_lpc_basecpld.ko"
        self.bmc_exist_cmd = "/sys/bus/platform/devices/sys_cpld/bmc_present"
        self.platform_name = "x86_64-cel_silverstone_v2-r0"
        self.bmc_present = False

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

    def get_kernel_path(self):
        """
        get the kernel object complete path
        :return:
        """
        sta_, res_ = self.run_command("uname -r")
        if sta_:
            return self.ker_path.format(res_)
        else:
            print("Can't get the kernel extra path!")
            return None

    def install_lpc_basecpld(self):
        """
        install lpc basecpld driver
        """
        ker_path = self.get_kernel_path()
        if ker_path:
            self.run_command("insmod %s/%s" % (ker_path, self.lpc_basecpld_ko))
            print("Has install %s" % self.lpc_basecpld_ko)
        else:
            print("Install %s error!" % self.lpc_basecpld_ko)

    def uninstall_lpc_basecpld(self):
        self.run_command("rmmod %s" % self.lpc_basecpld_name)
        print("Has remove %s" % self.lpc_basecpld_name)

    def get_bmc_status(self):
        """
        get bmc status and save bmc status to '/usr/local/bin/bmc_present'
        """
        self.install_lpc_basecpld()
        if os.path.exists(self.bmc_exist_cmd):
            # "1": "absent", "0": "present"
            sta, res = self.run_command("cat %s" % self.bmc_exist_cmd)
            self.bmc_present = True if res == "0" else False
        self.run_command("echo '%s' > /usr/local/bin/bmc_present" % self.bmc_present)
        self.uninstall_lpc_basecpld()

    def choose_pddf_device_json(self):
        """
        Depending on the state of the BMC, different pddf-device.json file configurations will be used:
        1.BMC exist: cp pddf-device.json-bmc pddf-device.json
        2.None BMC : cp pddf-device.json-nonebmc pddf-device.json
        """
        device_name = "pddf-device.json-bmc" if self.bmc_present else "pddf-device.json-nonebmc"
        device_path = "/usr/share/sonic/device/%s/pddf/" % self.platform_name
        self.run_command("cp %s%s %spddf-device.json" % (device_path, device_name, device_path))
        print("The selection of the %s file has been completed" % device_name)

    def main(self):
        self.get_bmc_status()
        self.choose_pddf_device_json()


if __name__ == '__main__':
    pre_init = PrePddfInit()
    pre_init.main()