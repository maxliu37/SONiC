#############################################################################
# Accton
#
# Thermal contains an implementation of SONiC Platform Base API and
# provides the thermal device status which are available in the platform
#
#############################################################################

import os
import os.path
import glob

try:
    from sonic_platform_base.thermal_base import ThermalBase
    from .helper import DeviceThreshold
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

PSU_I2C_PATH = "/sys/bus/i2c/devices/{}-00{}/"

PSU_HWMON_I2C_MAPPING = {
    0: {
        "num": 41,
        "addr": "59"
    },
    1: {
        "num": 33,
        "addr": "58"
    }
}

PSU_CPLD_I2C_MAPPING = {
    0: {
        "num": 41,
        "addr": "51"
    },
    1: {
        "num": 33,
        "addr": "50"
    }
}

THERMAL_NAME_LIST = ["Temp sensor 1", "Temp sensor 2", "Temp sensor 3",
                     "Temp sensor 4", "Temp sensor 5", "Temp sensor 6",
                     "Temp sensor 7", "Temp sensor 8", "Temp sensor 9",
                     "Temp sensor 10", "Temp sensor 11", "CPU Temp"]

PSU_THERMAL_NAME_LIST = ["PSU-1 temp sensor 1", "PSU-2 temp sensor 1"]

SYSFS_PATH = "/sys/bus/i2c/devices"
CPU_SYSFS_PATH = "/sys/devices/platform"

class Thermal(ThermalBase):
    """Platform-specific Thermal class"""

    def __init__(self, thermal_index=0, is_psu=False, psu_index=0):
        global psu_temp_max
        self.index = thermal_index
        self.is_psu = is_psu
        self.psu_index = psu_index
        self.min_temperature = None
        self.max_temperature = None

        if self.is_psu:
            psu_i2c_bus = PSU_HWMON_I2C_MAPPING[psu_index]["num"]
            psu_i2c_addr = PSU_HWMON_I2C_MAPPING[psu_index]["addr"]
            self.psu_hwmon_path = PSU_I2C_PATH.format(psu_i2c_bus,
                                                      psu_i2c_addr)
            psu_i2c_bus = PSU_CPLD_I2C_MAPPING[psu_index]["num"]
            psu_i2c_addr = PSU_CPLD_I2C_MAPPING[psu_index]["addr"]
            self.cpld_path = PSU_I2C_PATH.format(psu_i2c_bus, psu_i2c_addr)

        self.conf = DeviceThreshold(self.get_name())
        if self.is_psu:
            temp_file_path = self.psu_hwmon_path + "psu_temp1_max"
            psu_temp_max = self.__get_temp(temp_file_path)
        # Default thresholds
        self.default_threshold = {
            THERMAL_NAME_LIST[0] : {
                self.conf.HIGH_THRESHOLD_FIELD : '71.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '76.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[1] : {
                self.conf.HIGH_THRESHOLD_FIELD : '55.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '60.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[2] : {
                self.conf.HIGH_THRESHOLD_FIELD : '58.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '63.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[3] : {
                self.conf.HIGH_THRESHOLD_FIELD : '49.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '54.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[4] : {
                self.conf.HIGH_THRESHOLD_FIELD : '50.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '55.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[5] : {
                self.conf.HIGH_THRESHOLD_FIELD : '45.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '50.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[6] : {
                self.conf.HIGH_THRESHOLD_FIELD : '41.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '46.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[7] : {
                self.conf.HIGH_THRESHOLD_FIELD : '65.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '70.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[8] : {
                self.conf.HIGH_THRESHOLD_FIELD : '56.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '61.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[9] : {
                self.conf.HIGH_THRESHOLD_FIELD : '52.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '57.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[10] : {
                self.conf.HIGH_THRESHOLD_FIELD : '62.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '67.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            THERMAL_NAME_LIST[11] : {
                self.conf.HIGH_THRESHOLD_FIELD : '99.0',
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : '107.0',
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            PSU_THERMAL_NAME_LIST[0] : {
                self.conf.HIGH_THRESHOLD_FIELD : str(float(psu_temp_max)),
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            },
            PSU_THERMAL_NAME_LIST[1] : {
                self.conf.HIGH_THRESHOLD_FIELD : str(float(psu_temp_max)),
                self.conf.LOW_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.HIGH_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE,
                self.conf.LOW_CRIT_THRESHOLD_FIELD : self.conf.NOT_AVAILABLE
            }
        }

        # Set hwmon path
        i2c_path = {
            0: "2-0048/hwmon/hwmon*/",
            1: "2-0049/hwmon/hwmon*/",
            2: "14-004c/hwmon/hwmon*/",
            3: "27-0048/hwmon/hwmon*/",
            4: "27-0049/hwmon/hwmon*/",
            5: "34-0048/hwmon/hwmon*/",
            6: "42-0049/hwmon/hwmon*/",
            7: "57-0048/hwmon/hwmon*/",
            8: "58-004c/hwmon/hwmon*/",
            9: "65-004c/hwmon/hwmon*/",
            10: "66-004d/hwmon/hwmon*/",
            11: "coretemp.0/hwmon/hwmon*/"
        }.get(self.index, None)

        self.is_cpu = False
        if self.index == 11:
            self.is_cpu = True
            self.hwmon_path = "{}/{}".format(CPU_SYSFS_PATH, i2c_path)
        else:
            self.hwmon_path = "{}/{}".format(SYSFS_PATH, i2c_path)
        self.ss_key = THERMAL_NAME_LIST[self.index]
        self.ss_index = 1

    def __read_txt_file(self, file_path):
        for filename in glob.glob(file_path):
            try:
                with open(filename, 'r') as fd:
                    data =fd.readline().rstrip()
                    return data
            except IOError as e:
                pass

        return None

    def __get_temp(self, temp_file):
        if not self.is_psu:
            temp_file_path = os.path.join(self.hwmon_path, temp_file)
        else:
            temp_file_path = temp_file
        raw_temp = self.__read_txt_file(temp_file_path)
        if raw_temp is not None:
            return float(raw_temp)/1000
        else:
            return 80.0

    def __set_threshold(self, file_name, temperature):
        if self.is_psu:
            return True
        temp_file_path = os.path.join(self.hwmon_path, file_name)
        for filename in glob.glob(temp_file_path):
            try:
                with open(filename, 'w') as fd:
                    fd.write(str(temperature))
                return True
            except IOError as e:
                print("IOError")


    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal
        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        if not self.is_psu:
            temp_file = "temp{}_input".format(self.ss_index)
        else:
            temp_file = self.psu_hwmon_path + "psu_temp1_input"

        current = self.__get_temp(temp_file)
        if self.min_temperature is None or current < self.min_temperature:
            self.min_temperature = current

        if self.max_temperature is None or current > self.max_temperature:
            self.max_temperature = current

        return current

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal
        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        value = self.conf.get_high_threshold()
        if value != self.conf.NOT_AVAILABLE:
            return float(value)

        default_value = self.default_threshold[self.get_name()][self.conf.HIGH_THRESHOLD_FIELD]
        if default_value != self.conf.NOT_AVAILABLE:
            return float(default_value)

        raise NotImplementedError

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal
        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        try:
            value = float(temperature)
        except Exception:
            return False

        try:
            self.conf.set_high_threshold(str(value))
        except Exception:
            return False

        return True

    def get_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        if self.is_psu:
            return PSU_THERMAL_NAME_LIST[self.psu_index]
        else:
            return THERMAL_NAME_LIST[self.index]

    def get_presence(self):
        """
        Retrieves the presence of the Thermal
        Returns:
            bool: True if Thermal is present, False if not
        """
        if self.is_cpu:
            return True

        if self.is_psu:
            val = self.__read_txt_file(self.cpld_path + "psu_present")
            return int(val, 10) == 1
        temp_file = "temp{}_input".format(self.ss_index)
        temp_file_path = os.path.join(self.hwmon_path, temp_file)
        raw_txt = self.__read_txt_file(temp_file_path)
        if raw_txt is not None:
            return True
        else:
            return False


    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        if self.is_cpu:
            return True

        if self.is_psu:
            temp_file = self.psu_hwmon_path + "psu_temp1_input"
            return self.get_presence() and (int(
                self.__read_txt_file(temp_file)))

        file_str = "temp{}_input".format(self.ss_index)
        file_path = os.path.join(self.hwmon_path, file_str)
        raw_txt = self.__read_txt_file(file_path)
        if raw_txt is None:
            return False
        else:
            return int(raw_txt) != 0

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device
        Returns:
            string: Model/part number of device
        """

        return "N/A"

    def get_serial(self):
        """
        Retrieves the serial number of the device
        Returns:
            string: Serial number of device
        """
        return "N/A"

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device. If the agent cannot determine the parent-relative position
        for some reason, or if the associated value of entPhysicalContainedIn is '0', then the value '-1' is returned
        Returns:
            integer: The 1-based relative physical position in parent device or -1 if cannot determine the position
        """
        return self.index+1

    def is_replaceable(self):
        """
        Retrieves whether thermal module is replaceable
        Returns:
            A boolean value, True if replaceable, False if not
        """
        return False

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold temperature of thermal by 1-based index
        Actions should be taken immediately if the temperature becomes higher than the high critical
        threshold otherwise the device will be damaged.

        :param index: An integer, 1-based index of the thermal sensor of which to query status
        :return: A float number, the high critical threshold temperature of thermal in Celsius
                 up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        value = self.conf.get_high_critical_threshold()
        if value != self.conf.NOT_AVAILABLE:
            return float(value)

        default_value = self.default_threshold[self.get_name()][self.conf.HIGH_CRIT_THRESHOLD_FIELD]
        if default_value != self.conf.NOT_AVAILABLE:
            return float(default_value)

        raise NotImplementedError

    def set_high_critical_threshold(self, temperature):
        """
        Sets the critical high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        try:
            value = float(temperature)
        except Exception:
            return False

        try:
            self.conf.set_high_critical_threshold(str(value))
        except Exception:
            return False

        return True

    def get_minimum_recorded(self):
        """ Retrieves the minimum recorded temperature of thermal
        Returns: A float number, the minimum recorded temperature of thermal in Celsius
        up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self.min_temperature is None:
            self.get_temperature()

        return self.min_temperature

    def get_maximum_recorded(self):
        """ Retrieves the maximum recorded temperature of thermal
        Returns: A float number, the maximum recorded temperature of thermal in Celsius
        up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self.max_temperature is None:
            self.get_temperature()

        return self.max_temperature

