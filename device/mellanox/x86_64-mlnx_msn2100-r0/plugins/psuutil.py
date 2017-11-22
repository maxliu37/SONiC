#!/usr/bin/env python

#############################################################################
# Mellanox
#
# Module contains an implementation of SONiC PSU Base API and
# provides the PSUs status which are available in the platform
#
#############################################################################

import os.path

try:
    from sonic_psu.psu_base import PsuBase
except ImportError, e:
    raise ImportError (str(e) + "- required module not found")

class PsuUtil(PsuBase):
    """Platform-specific PSUutil class"""

    def __init__(self):
        PsuBase.__init__(self)

        self.psu_path = "/sys/bus/i2c/devices/2-0060/"
        self.psu_presence = "psu{}_status"
        self.psu_oper_status = "psu{}_pg_status"

    def get_num_psus(self):
        """
        Retrieves the number of PSUs available on the device

        :return: An integer, the number of PSUs available on the device
        """
        return 2

    def get_psu_status(self, index):
        """
        Retrieves the oprational status of power supply unit (PSU) defined
                by index <index>

        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is operating properly, False if PSU is faulty
        """
        if index is None:
            return False

        status = 0
        with open(self.psu_path + self.psu_oper_status.format(index), 'r') as power_status:
            status = int(power_status.read())

        return status == 1

    def get_psu_presence(self, index):
        """
        Retrieves the presence status of power supply unit (PSU) defined
                by index <index>

        :param index: An integer, index of the PSU of which to query status
        :return: Boolean, True if PSU is plugged, False if not
        """
        if index is None:
            return False

        status = 0
        with open(self.psu_path + self.psu_presence.format(index), 'r') as presence_status:
            status = int(presence_status.read())

        return status == 1
