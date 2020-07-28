#!/usr/bin/env python

########################################################################
# Marvell
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Thermals' information which are available in the platform
#
########################################################################


try:
    import os
    from sonic_platform_base.thermal_base import ThermalBase
    from sonic_platform.psu import Psu
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Thermal(ThermalBase):
    """Marvell platform-specific Thermal class"""

    I2C_DIR = "/sys/class/i2c-adapter/"
    I2C_DEV_MAPPING = (['i2c-7/7-0049/hwmon/', 1],
                       ['i2c-7/7-004a/hwmon/', 1],
                       ['i2c-7/7-004b/hwmon/', 1],
                       ['i2c-7/7-004c/hwmon/', 1])

    THERMAL_NAME = ('ASIC On-board', 'CPU Complex', 'System Front', 'System Rear',
                    'CPU Core')

    def __init__(self, thermal_index):
        self.index = thermal_index + 1
        self.is_psu_thermal = False
        self.dependency = None

        if self.index < 5:
            i2c_path = self.I2C_DIR + self.I2C_DEV_MAPPING[self.index - 1][0]
            hwmon_temp_index = self.I2C_DEV_MAPPING[self.index - 1][1]
            hwmon_temp_suffix = "max"
            hwmon_node = os.listdir(i2c_path)[0]
            self.HWMON_DIR = i2c_path + hwmon_node + '/'

        else:
            dev_path = "/sys/devices/platform/coretemp.0/hwmon/"
            hwmon_temp_index = self.index - 4
            hwmon_temp_suffix = "crit"
            hwmon_node = os.listdir(dev_path)[0]
            self.HWMON_DIR = dev_path + hwmon_node + '/'

        self.thermal_temperature_file = self.HWMON_DIR \
            + "temp{}_input".format(hwmon_temp_index)
        self.thermal_high_threshold_file = self.HWMON_DIR \
            + "temp{}_{}".format(hwmon_temp_index, hwmon_temp_suffix)

    def _read_sysfs_file(self, sysfs_file):
        # On successful read, returns the value read from given
        # sysfs_file and on failure returns 'ERR'
        rv = 'ERR'

        if (not os.path.isfile(sysfs_file)):
            return rv

        try:
            with open(sysfs_file, 'r') as fd:
                rv = fd.read()
        except:
            rv = 'ERR'

        rv = rv.rstrip('\r\n')
        rv = rv.lstrip(" ")
        return rv

    def get_name(self):
        """
        Retrieves the name of the thermal

        Returns:
            string: The name of the thermal
        """
        return self.THERMAL_NAME[self.index - 1]

    def get_presence(self):
        """
        Retrieves the presence of the thermal

        Returns:
            bool: True if thermal is present, False if not
        """
        if self.dependency:
            return self.dependency.get_presence()
        else:
            return True

    def get_model(self):
        """
        Retrieves the model number (or part number) of the Thermal

        Returns:
            string: Model/part number of Thermal
        """
        return 'NA'

    def get_serial(self):
        """
        Retrieves the serial number of the Thermal

        Returns:
            string: Serial number of Thermal
        """
        return 'NA'

    def get_status(self):
        """
        Retrieves the operational status of the thermal

        Returns:
            A boolean value, True if thermal is operating properly,
            False if not
        """
        if self.dependency:
            return self.dependency.get_status()
        else:
            return True

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal

        Returns:
            A float number of current temperature in Celsius up to
            nearest thousandth of one degree Celsius, e.g. 30.125
        """
        thermal_temperature = self._read_sysfs_file(
            self.thermal_temperature_file)
        if (thermal_temperature != 'ERR'):
            thermal_temperature = float(thermal_temperature) / 1000
        else:
            thermal_temperature = 0

        return "{:.3f}".format(thermal_temperature)

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal

        Returns:
            A float number, the high threshold temperature of thermal in
            Celsius up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        """
        thermal_high_threshold = self._read_sysfs_file(
            self.thermal_high_threshold_file)
        if (thermal_high_threshold != 'ERR'):
            thermal_high_threshold = float(thermal_high_threshold) / 1000
        else:
            thermal_high_threshold = 0

        return "{:.3f}".format(thermal_high_threshold)

    def get_low_threshold(self):
        """
        Retrieves the low threshold temperature of thermal

        Returns:
            A float number, the low threshold temperature of thermal in
            Celsius up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        """
        thermal_low_threshold = 0
        return "{:.3f}".format(thermal_low_threshold)

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one
            degree Celsius, e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if
            not
        """
        # Thermal threshold values are pre-defined based on HW.
        return False

    def set_low_threshold(self, temperature):
        """
        Sets the low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one
            degree Celsius, e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if
            not
        """
        # Thermal threshold values are pre-defined based on HW.
        return False

