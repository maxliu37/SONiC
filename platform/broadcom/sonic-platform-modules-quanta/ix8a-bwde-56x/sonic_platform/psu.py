#!/usr/bin/env python
#
# Name: psu.py, version: 1.0
#
# Description: Module contains the definitions of SONiC platform APIs
#

try:
    import logging
    import os
    from sonic_platform_base.psu_base import PsuBase
    from sonic_platform.fan import Fan
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

HWMON_DIR = "/sys/class/hwmon/hwmon2/"

class Psu(PsuBase):
    def __init__(self, index):
        PsuBase.__init__(self)
        fan = Fan(index, True)
        self._fan_list.append(fan)

        self.index                = index
        self.psu_presence_attr    = "PSU{}_POWER_OUT_present".format(self.index)
        self.psu_status_attr      = "PSU{}_CURRENT_OUT_input".format(self.index)
        self.psu_power_in_attr    = "PSU{}_POWER_IN_input".format(self.index)
        self.psu_power_out_attr   = "PSU{}_POWER_OUT_input".format(self.index)
        self.psu_voltage_out_attr = "PSU{}_VOLTAGE_OUT_input".format(self.index)
        self.psu_current_out_attr = "PSU{}_CURRENT_OUT_input".format(self.index)
        self.psu_voltage_in_attr  = "PSU{}_VOLTAGE_IN_input".format(self.index)
        self.psu_current_in_attr  = "PSU{}_CURRENT_IN_input".format(self.index)
        self.psu_serial_attr      = "PSU{}_POWER_OUT_sn".format(self.index)
        self.psu_model_attr       = "PSU{}_POWER_OUT_model".format(self.index)
        self.psu_mfr_id_attr      = "PSU{}_POWER_OUT_mfrid".format(self.index)
        self.psu_capacity_attr    = "PSU{}_POWER_OUT_pout_max".format(self.index)
        self.psu_type_attr        = "PSU{}_POWER_OUT_vin_type".format(self.index)

    def __get_attr_value(self, attr_path):

        retval = 'ERR'
        if (not os.path.isfile(attr_path)):
            return retval

        try:
            with open(attr_path, 'r') as fd:
                retval = fd.read()
        except Exception as error:
            logging.error("Unable to open " + attr_path + " file !")

        retval = retval.rstrip(' \t\n\r')
        fd.close()
        return retval

##############################################
# Device methods
##############################################

    def get_name(self):
        """
        Retrieves the name of the device

        Returns:
            string: The name of the device
        """
        return "PSU{}".format(self.index)

    def get_presence(self):
        """
        Retrieves the presence of the device

        Returns:
            bool: True if device is present, False if not
        """
        presence = False
        attr_path = HWMON_DIR+self.psu_presence_attr
        attr_normal = '1'

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            if (attr_rv == attr_normal):
                presence = True

        return presence

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device

        Returns:
            string: Model/part number of device
        """
        model = "N/A"
        attr_path = HWMON_DIR+self.psu_model_attr
        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            model = attr_rv

        return model

    def get_mfr_id(self):
        """
        Retrieves the manufacturer's name (or id) of the device

        Returns:
            string: Manufacturer's id of device
        """
        mfr_id = "N/A"
        attr_path = HWMON_DIR+self.psu_mfr_id_attr
        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            mfr_id = attr_rv

        return mfr_id

    def get_serial(self):
        """
        Retrieves the serial number of the device

        Returns:
            string: Serial number of device
        """
        serial = "N/A"
        attr_path = HWMON_DIR+self.psu_serial_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            serial = attr_rv

        return serial

    def get_status(self):
        """
        Retrieves the operational status of the device

        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        status = False
        attr_path = HWMON_DIR+self.psu_status_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            if (int(attr_rv) != 0):
                status = True

        return status

##############################################
# PSU methods
##############################################

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """
        voltage_out = 0.0
        attr_path = HWMON_DIR+self.psu_voltage_out_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            voltage_out = float(attr_rv) / 1000

        return voltage_out

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        current_out = 0.0
        attr_path = HWMON_DIR+self.psu_current_out_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            current_out = float(attr_rv) / 1000

        return current_out

    def get_input_voltage(self):
        """
        Retrieves current PSU voltage input

        Returns:
            A float number, the input voltage in volts,
            e.g. 12.1
        """
        voltage_in = 0.0
        attr_path = HWMON_DIR+self.psu_voltage_in_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            voltage_in = float(attr_rv) / 1000

        return voltage_in

    def get_input_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        current_in = 0.0
        attr_path = HWMON_DIR+self.psu_current_in_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            current_in = float(attr_rv) / 1000

        return current_in

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts, e.g. 302.6
        """
        power_out = 0.0
        attr_path = HWMON_DIR+self.psu_power_out_attr

        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            attr_rv, dummy = attr_rv.split('.', 1)
            power_out = float(attr_rv) / 1000

        return power_out

    def get_powergood_status(self):
        """
        Retrieves the powergood status of PSU

        Returns:
            A boolean, True if PSU has stablized its output voltages and passed all
            its internal self-tests, False if not.
        """
        return self.get_status()

    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings above
        """
        if self.get_powergood_status():
            return self.STATUS_LED_COLOR_GREEN
        else:
            return self.STATUS_LED_COLOR_OFF

    def get_type(self):
        """
        Gets the type of the PSU

        Returns:
            A string, the type of PSU (AC/DC)
        """
        type = "AC"
        attr_path = HWMON_DIR+self.psu_type_attr
        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            type = attr_rv

        return type

    def get_capacity(self):
        """
        Gets the capacity (maximum output power) of the PSU in watts

        Returns:
            An integer, the capacity of PSU
        """
        capacity = 0
        attr_path = HWMON_DIR+self.psu_capacity_attr
        attr_rv = self.__get_attr_value(attr_path)
        if (attr_rv != 'ERR'):
            try:
                capacity = int(attr_rv)
            except ValueError:
                capacity = 0

        return capacity

