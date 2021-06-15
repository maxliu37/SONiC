#!/usr/bin/env python

#############################################################################
# Mellanox
#
# Module contains an implementation of SONiC Platform Base API and
# provides the PSUs status which are available in the platform
#
#############################################################################

try:
    import os
    from sonic_platform_base.psu_base import PsuBase
    from sonic_py_common.logger import Logger
    from .led import PsuLed, SharedLed, ComponentFaultyIndicator
    from . import utils
    from .vpd_parser import VpdParser
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")


# Global logger class instance
logger = Logger()

PSU_PATH = '/var/run/hw-management/'


class FixedPsu(PsuBase):
    def __init__(self, psu_index):
        super(FixedPsu, self).__init__()
        self.index = psu_index + 1
        self._name = "PSU {}".format(self.index)
        self.psu_oper_status = os.path.join(PSU_PATH, "thermal/psu{}_pwr_status".format(self.index))
        self._led = None

    def get_name(self):
        return self._name

    def get_model(self):
        return ''

    def get_serial(self):
        return ''

    def get_revision(self):
        return ''

    def get_powergood_status(self):
        """
        Retrieves the operational status of power supply unit (PSU) defined

        Returns:
            bool: True if PSU is operating properly, False if not
        """
        return utils.read_int_from_file(self.psu_oper_status) == 1

    def get_presence(self):
        """
        Retrieves the presence status of power supply unit (PSU) defined

        Returns:
            bool: True if PSU is present, False if not
        """
        return True

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts, 
            e.g. 12.1 
        """
        return None

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        return None

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts, e.g. 302.6
        """
        return None

    @property
    def led(self):
        if not self._led:
            self._led = PsuLed(self.index)
        return self._led

    def set_status_led(self, color):
        """
        Sets the state of the PSU status LED

        Args:
            color: A string representing the color with which to set the
                   PSU status LED

        Returns:
            bool: True if status LED state is set successfully, False if not

        Notes:
            Only one led for all PSUs.
        """
        return self.led.set_status(color)

    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings above
        """
        return self.led.get_status()

    def get_power_available_status(self):
        """
        Gets the power available status

        Returns:
            True if power is present and power on. 
            False and "absence of PSU" if power is not present.
            False and "absence of power" if power is present but not power on.
        """
        if not self.get_presence():
            return False, "absence of PSU"
        elif not self.get_powergood_status():
            return False, "absence of power"
        else:
            return True, ""

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device
        Returns:
            integer: The 1-based relative physical position in parent device
        """
        return self.index

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False

    def get_temperature(self):
        """
        Retrieves current temperature reading from PSU

        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125 
        """
        return None

    def get_temperature_high_threshold(self):
        """
        Retrieves the high threshold temperature of PSU

        Returns:
            A float number, the high threshold temperature of PSU in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return None

    def get_voltage_high_threshold(self):
        """
        Retrieves the high threshold PSU voltage output

        Returns:
            A float number, the high threshold output voltage in volts, 
            e.g. 12.1 
        """
        # hw-management doesn't expose those sysfs for now
        raise NotImplementedError

    def get_voltage_low_threshold(self):
        """
        Retrieves the low threshold PSU voltage output

        Returns:
            A float number, the low threshold output voltage in volts, 
            e.g. 12.1 
        """
        # hw-management doesn't expose those sysfs for now
        raise NotImplementedError
     
class Psu(FixedPsu):
    """Platform-specific Psu class"""
    PSU_CURRENT = "power/psu{}_curr"
    PSU_VOLTAGE = "power/psu{}_volt"
    PSU_VOLTAGE1 = "power/psu{}_volt_out2"
    PSU_POWER = "power/psu{}_power"
    PSU_VPD = "eeprom/psu{}_vpd"
    shared_led = None

    def __init__(self, psu_index):
        super(Psu, self).__init__(psu_index)

        psu_voltage = os.path.join(PSU_PATH, self.PSU_VOLTAGE1.format(self.index))
        # Workaround for psu voltage sysfs file as the file name differs among platforms
        if os.path.exists(psu_voltage):
            self.psu_voltage = os.path.join(PSU_PATH, self.PSU_VOLTAGE1.format(self.index))
        else:
            self.psu_voltage = os.path.join(PSU_PATH, self.PSU_VOLTAGE.format(self.index))

        self.psu_current = os.path.join(PSU_PATH, self.PSU_CURRENT.format(self.index))
        self.psu_power = os.path.join(PSU_PATH, self.PSU_POWER.format(self.index))
        self.psu_presence = os.path.join(PSU_PATH, "thermal/psu{}_status".format(self.index))

        self.psu_temp = os.path.join(PSU_PATH, 'thermal/psu{}_temp'.format(self.index))
        self.psu_temp_threshold = os.path.join(PSU_PATH, 'thermal/psu{}_temp_max'.format(self.index))

        from .fan import PsuFan
        self._fan_list.append(PsuFan(psu_index, 1, self))

        self.vpd_parser = VpdParser(os.path.join(PSU_PATH, self.PSU_VPD.format(self.index)))

        # initialize thermal for PSU
        from .thermal import initialize_psu_thermal
        initialize_psu_thermal(self.index)

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device

        Returns:
            string: Model/part number of device
        """
        return self.vpd_parser.get_model()

    def get_serial(self):
        """
        Retrieves the serial number of the device

        Returns:
            string: Serial number of device
        """
        return self.vpd_parser.get_serial()

    def get_revision(self):
        """
        Retrieves the hardware revision of the device

        Returns:
            string: Revision value of device
        """
        return self.vpd_parser.get_revision()

    def get_presence(self):
        """
        Retrieves the presence status of power supply unit (PSU) defined

        Returns:
            bool: True if PSU is present, False if not
        """
        return utils.read_int_from_file(self.psu_presence) == 1

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts, 
            e.g. 12.1 
        """
        if self.get_powergood_status():
            voltage = utils.read_int_from_file(self.psu_voltage)
            return float(voltage) / 1000
        return None

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        if self.get_powergood_status():
            amperes = utils.read_int_from_file(self.psu_current)
            return float(amperes) / 1000
        return None

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts, e.g. 302.6
        """
        if self.get_powergood_status():
            power = utils.read_int_from_file(self.psu_power)
            return float(power) / 1000000
        return None

    @classmethod
    def get_shared_led(cls):
        if not cls.shared_led:
            cls.shared_led = SharedLed(PsuLed(None))
        return cls.shared_led

    @property
    def led(self):
        if not self._led:
            self._led = ComponentFaultyIndicator(Psu.get_shared_led())
        return self._led

    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings above
        """
        return Psu.get_shared_led().get_status()

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return True

    def get_temperature(self):
        """
        Retrieves current temperature reading from PSU

        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125 
        """
        if self.get_powergood_status():
            temp = utils.read_int_from_file(self.psu_temp)
            return float(temp) / 1000

        return None

    def get_temperature_high_threshold(self):
        """
        Retrieves the high threshold temperature of PSU

        Returns:
            A float number, the high threshold temperature of PSU in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self.get_powergood_status():
            temp_threshold = utils.read_int_from_file(self.psu_temp_threshold)
            return float(temp_threshold) / 1000

        return None
