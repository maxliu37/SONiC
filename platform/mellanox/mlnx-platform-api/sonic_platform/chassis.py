#!/usr/bin/env python

#############################################################################
# Mellanox
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Chassis information which are available in the platform
#
#############################################################################

try:
    from sonic_platform_base.chassis_base import ChassisBase
    from sonic_py_common.logger import Logger
    import glob
    import os
    import sys
    from functools import reduce

    from .device_data import DeviceDataManager
    from . import utils
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

MAX_SELECT_DELAY = 3600

DMI_FILE = '/sys/firmware/dmi/entries/2-0/raw'
DMI_HEADER_LEN = 15
DMI_PRODUCT_NAME = "Product Name"
DMI_MANUFACTURER = "Manufacturer"
DMI_VERSION = "Version"
DMI_SERIAL = "Serial Number"
DMI_ASSET_TAG = "Asset Tag"
DMI_LOC = "Location In Chassis"
DMI_TABLE_MAP = {
                    DMI_PRODUCT_NAME: 0,
                    DMI_MANUFACTURER: 1,
                    DMI_VERSION: 2,
                    DMI_SERIAL: 3,
                    DMI_ASSET_TAG: 4,
                    DMI_LOC: 5
                }

HWMGMT_SYSTEM_ROOT = '/var/run/hw-management/system/'

#reboot cause related definitions
REBOOT_CAUSE_ROOT = HWMGMT_SYSTEM_ROOT

REBOOT_CAUSE_FILE_LENGTH = 1

# Global logger class instance
logger = Logger()


class Chassis(ChassisBase):
    """Platform-specific Chassis class"""

    # System status LED
    _led = None

    def __init__(self):
        super(Chassis, self).__init__()

        # Initialize DMI data
        self.dmi_data = None
        
        # move the initialization of each components to their dedicated initializer
        # which will be called from platform
        #
        # Multiple scenarios need to be taken into consideration regarding the SFP modules initialization.
        # - Platform daemons
        #   - Can access multiple or all SFP modules
        # - sfputil
        #   - Sometimes can access only one SFP module
        #   - Call get_sfp to get one SFP module object
        #
        # We should initialize all SFP modules only if it is necessary because initializing SFP module is time-consuming.
        # This means,
        # - If get_sfp is called,
        #    - If the _sfp_list isn't initialized, initialize it first.
        #    - Only the SFP module being required should be initialized.
        # - If get_all_sfps is called,
        #    - If the _sfp_list isn't initialized, initialize it first.
        #    - All SFP modules need to be initialized.
        #      But the SFP modules that have already been initialized should not be initialized for the second time.
        #      This can caused by get_sfp being called before.
        #
        # Due to the complexity of SFP modules initialization, we have to introduce two initialized flags for SFP modules
        # - sfp_module_partial_initialized:
        #    - False: The _sfp_list is [] (SFP stuff has never been accessed)
        #    - True: The _sfp_list is a list whose length is number of SFP modules supported by the platform
        # - sfp_module_full_initialized:
        #    - False: All SFP modules have not been created
        #    - True: All SFP modules have been created
        #
        self.sfp_initialized_count = 0
        self.sfp_event = None
        self.reboot_cause_initialized = False
        logger.log_info("Chassis loaded successfully")

    def __del__(self):
        if self.sfp_event:
            self.sfp_event.deinitialize()

        from .sfp import SFP, deinitialize_sdk_handle
        if SFP.shared_sdk_handle:
            deinitialize_sdk_handle(SFP.shared_sdk_handle)
        
    ##############################################
    # PSU methods
    ##############################################

    def initialize_psu(self):
        if not self._psu_list:
            from .psu import Psu, FixedPsu
            psu_count = DeviceDataManager.get_psu_count()
            hot_swapable = DeviceDataManager.is_psu_hotswapable()

            # Initialize PSU list
            for index in range(psu_count):
                if hot_swapable:
                    psu = Psu(index)
                else:
                    psu = FixedPsu(index)
                self._psu_list.append(psu)

    @utils.pre_initialize(initialize_psu)
    def get_num_psus(self):
        """
        Retrieves the number of power supply units available on this chassis

        Returns:
            An integer, the number of power supply units available on this
            chassis
        """
        return len(self._psu_list)

    @utils.pre_initialize(initialize_psu)
    def get_all_psus(self):
        """
        Retrieves all power supply units available on this chassis

        Returns:
            A list of objects derived from PsuBase representing all power
            supply units available on this chassis
        """
        return self._psu_list

    @utils.pre_initialize(initialize_psu)
    def get_psu(self, index):
        """
        Retrieves power supply unit represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the power supply unit to
            retrieve

        Returns:
            An object dervied from PsuBase representing the specified power
            supply unit
        """
        psu = None

        try:
            psu = self._psu_list[index]
        except IndexError:
            sys.stderr.write("PSU index {} out of range (0-{})\n".format(
                             index, len(self._psu_list)-1))

        return psu

    ##############################################
    # Fan methods
    ##############################################

    def initialize_fan(self):
        if not self._fan_drawer_list:
            from .fan import Fan
            from .fan_drawer import RealDrawer, VirtualDrawer

            hot_swapable = DeviceDataManager.is_fan_hotswapable()
            drawer_num = DeviceDataManager.get_fan_drawer_count()
            fan_num = DeviceDataManager.get_fan_count()
            fan_num_per_drawer = fan_num / drawer_num
            drawer_ctor = RealDrawer if hot_swapable else VirtualDrawer
            fan_index = 0
            for drawer_index in range(drawer_num):
                drawer = drawer_ctor(drawer_index)
                self._fan_drawer_list.append(drawer)
                for index in range(fan_num_per_drawer):
                    fan = Fan(fan_index, drawer, index + 1)
                    fan_index += 1
                    drawer._fan_list.append(fan)

    def get_num_fan_drawers(self):
        """
        Retrieves the number of fan drawers available on this chassis

        Returns:
            An integer, the number of fan drawers available on this chassis
        """
        return DeviceDataManager.get_fan_drawer_count()

    @utils.pre_initialize(initialize_fan)
    def get_all_fan_drawers(self):
        """
        Retrieves all fan drawers available on this chassis

        Returns:
            A list of objects derived from FanDrawerBase representing all fan
            drawers available on this chassis
        """
        return self._fan_drawer_list

    @utils.pre_initialize(initialize_fan)
    def get_fan_drawer(self, index):
        """
        Retrieves fan drawers represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the fan drawer to
            retrieve

        Returns:
            An object dervied from FanDrawerBase representing the specified fan
            drawer
        """
        fan_drawer = None

        try:
            fan_drawer = self._fan_drawer_list[index]
        except IndexError:
            sys.stderr.write("Fan drawer index {} out of range (0-{})\n".format(
                             index, len(self._fan_drawer_list)-1))

        return fan_drawer

    ##############################################
    # SFP methods
    ##############################################

    def initialize_single_sfp(self, index):
        index = index - 1
        sfp_count = self.get_num_sfps()
        if index < sfp_count:
            if not self._sfp_list:
                self._sfp_list = [None] * sfp_count
            
            if not self._sfp_list[index]:
                from .sfp import SFP
                self._sfp_list[index] = SFP(index)
                self.sfp_initialized_count += 1

    def initialize_sfp(self):
        if not self._sfp_list:
            from .sfp import SFP
            sfp_count = self.get_num_sfps()
            for index in range(sfp_count):
                sfp_module = SFP(index)
                self._sfp_list.append(sfp_module)
            self.sfp_initialized_count = sfp_count
        elif self.sfp_initialized_count != len(self._sfp_list):
            from .sfp import SFP
            for index in range(len(self._sfp_list)):
                if self._sfp_list[index] is None:
                    self._sfp_list[index] = SFP(index)
            self.sfp_initialized_count = len(self._sfp_list)

    def get_num_sfps(self):
        """
        Retrieves the number of sfps available on this chassis

        Returns:
            An integer, the number of sfps available on this chassis
        """
        return DeviceDataManager.get_sfp_count()

    @utils.pre_initialize(initialize_sfp)
    def get_all_sfps(self):
        """
        Retrieves all sfps available on this chassis

        Returns:
            A list of objects derived from SfpBase representing all sfps
            available on this chassis
        """
        return self._sfp_list

    @utils.pre_initialize_one(initialize_single_sfp)
    def get_sfp(self, index):
        """
        Retrieves sfp represented by (1-based) index <index>

        Args:
            index: An integer, the index (1-based) of the sfp to retrieve.
                   The index should be the sequence of a physical port in a chassis,
                   starting from 1.
                   For example, 1 for Ethernet0, 2 for Ethernet4 and so on.

        Returns:
            An object dervied from SfpBase representing the specified sfp
        """
        sfp = None
        index -= 1
        try:
            sfp = self._sfp_list[index]
        except IndexError:
            sys.stderr.write("SFP index {} out of range (0-{})\n".format(
                             index, len(self._sfp_list)-1))

        return sfp
        
    @utils.pre_initialize(initialize_sfp)
    def get_change_event(self, timeout=0):
        """
        Returns a nested dictionary containing all devices which have
        experienced a change at chassis level

        Args:
            timeout: Timeout in milliseconds (optional). If timeout == 0,
                this method will block until a change is detected.

        Returns:
            (bool, dict):
                - True if call successful, False if not;
                - A nested dictionary where key is a device type,
                  value is a dictionary with key:value pairs in the format of
                  {'device_id':'device_event'}, 
                  where device_id is the device ID for this device and
                        device_event,
                             status='1' represents device inserted,
                             status='0' represents device removed.
                  Ex. {'fan':{'0':'0', '2':'1'}, 'sfp':{'11':'0'}}
                      indicates that fan 0 has been removed, fan 2
                      has been inserted and sfp 11 has been removed.
        """
        # Initialize SFP event first
        if not self.sfp_event:
            from .sfp_event import sfp_event
            self.sfp_event = sfp_event()
            self.sfp_event.initialize()

        wait_for_ever = (timeout == 0)
        port_dict = {}
        if wait_for_ever:
            timeout = MAX_SELECT_DELAY
            while True:
                status = self.sfp_event.check_sfp_status(port_dict, timeout)
                if bool(port_dict):
                    break
        else:
            status = self.sfp_event.check_sfp_status(port_dict, timeout)

        if status:
            self.reinit_sfps(port_dict)
            return True, {'sfp':port_dict}
        else:
            return True, {'sfp':{}}

    def reinit_sfps(self, port_dict):
        """
        Re-initialize SFP if there is any newly inserted SFPs
        :param port_dict: SFP event data
        :return:
        """
        from . import sfp
        for index, status in port_dict.items():
            if status == sfp.SFP_STATUS_INSERTED:
                try:
                    self._sfp_list[index - 1].reinit()
                except Exception as e:
                    logger.log_error("Fail to re-initialize SFP {} - {}".format(index, repr(e)))

    @utils.pre_initialize(initialize_sfp)
    def _show_capabilities(self):
        """
        This function is for debug purpose
        Some features require a xSFP module to support some capabilities but it's unrealistic to
        check those modules one by one.
        So this function is introduce to show some capabilities of all xSFP modules mounted on the device.
        """
        for s in self._sfp_list:
            try:
                print("index {} tx disable {} dom {} calibration {} temp {} volt {} power (tx {} rx {})".format(s.index,
                    s.dom_tx_disable_supported,
                    s.dom_supported,
                    s.calibration,
                    s.dom_temp_supported,
                    s.dom_volt_supported,
                    s.dom_rx_power_supported,
                    s.dom_tx_power_supported
                    ))
            except:
                print("fail to retrieve capabilities for module index {}".format(s.index))

    ##############################################
    # THERMAL methods
    ##############################################

    def initialize_thermals(self):
        if not self._thermal_list:
            from .thermal import initialize_chassis_thermals
            # Initialize thermals
            self._thermal_list = initialize_chassis_thermals()

    @utils.pre_initialize(initialize_thermals)
    def get_num_thermals(self):
        """
        Retrieves the number of thermals available on this chassis

        Returns:
            An integer, the number of thermals available on this chassis
        """
        return len(self._thermal_list)

    @utils.pre_initialize(initialize_thermals)
    def get_all_thermals(self):
        """
        Retrieves all thermals available on this chassis

        Returns:
            A list of objects derived from ThermalBase representing all thermals
            available on this chassis
        """
        return self._thermal_list

    @utils.pre_initialize(initialize_thermals)
    def get_thermal(self, index):
        """
        Retrieves thermal unit represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the thermal to
            retrieve

        Returns:
            An object dervied from ThermalBase representing the specified thermal
        """
        thermal = None

        try:
            thermal = self._thermal_list[index]
        except IndexError:
            sys.stderr.write("THERMAL index {} out of range (0-{})\n".format(
                             index, len(self._thermal_list)-1))

        return thermal

    ##############################################
    # EEPROM methods
    ##############################################

    def initialize_eeprom(self):
        if not self._eeprom:
            from .eeprom import Eeprom
            # Initialize EEPROM
            self._eeprom = Eeprom()

    @utils.pre_initialize(initialize_eeprom)
    def get_eeprom(self):
        """
        Retreives eeprom device on this chassis

        Returns:
            An object derived from WatchdogBase representing the hardware
            eeprom device
        """
        return self._eeprom

    @utils.pre_initialize(initialize_eeprom)
    def get_name(self):
        """
        Retrieves the name of the device

        Returns:
            string: The name of the device
        """
        return self._eeprom.get_product_name()

    @utils.pre_initialize(initialize_eeprom)
    def get_model(self):
        """
        Retrieves the model number (or part number) of the device

        Returns:
            string: Model/part number of device
        """
        return self._eeprom.get_part_number()

    @utils.pre_initialize(initialize_eeprom)
    def get_base_mac(self):
        """
        Retrieves the base MAC address for the chassis

        Returns:
            A string containing the MAC address in the format
            'XX:XX:XX:XX:XX:XX'
        """
        return self._eeprom.get_base_mac()

    @utils.pre_initialize(initialize_eeprom)
    def get_serial(self):
        """
        Retrieves the hardware serial number for the chassis

        Returns:
            A string containing the hardware serial number for this chassis.
        """
        return self._eeprom.get_serial_number()

    @utils.pre_initialize(initialize_eeprom)
    def get_system_eeprom_info(self):
        """
        Retrieves the full content of system EEPROM information for the chassis

        Returns:
            A dictionary where keys are the type code defined in
            OCP ONIE TlvInfo EEPROM format and values are their corresponding
            values.
        """
        return self._eeprom.get_system_eeprom_info()

    ##############################################
    # Component methods
    ##############################################

    def initialize_components(self):
        if not self._component_list:
            # Initialize component list
            from .component import ComponentONIE, ComponentSSD, ComponentBIOS, ComponentCPLD
            self._component_list.append(ComponentONIE())
            self._component_list.append(ComponentSSD())
            self._component_list.append(ComponentBIOS())
            self._component_list.extend(ComponentCPLD.get_component_list())

    @utils.pre_initialize(initialize_components)
    def get_num_components(self):
        """
        Retrieves the number of components available on this chassis

        Returns:
            An integer, the number of components available on this chassis
        """
        return len(self._component_list)

    @utils.pre_initialize(initialize_components)
    def get_all_components(self):
        """
        Retrieves all components available on this chassis

        Returns:
            A list of objects derived from ComponentBase representing all components
            available on this chassis
        """
        return self._component_list

    @utils.pre_initialize(initialize_components)
    def get_component(self, index):
        """
        Retrieves component represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the component to retrieve

        Returns:
            An object dervied from ComponentBase representing the specified component
        """
        component = None

        try:
            component = self._component_list[index]
        except IndexError:
            sys.stderr.write("Component index {} out of range (0-{})\n".format(
                             index, len(self._component_list)-1))

        return component

    ##############################################
    # System LED methods
    ##############################################

    def initizalize_system_led(self):
        if not Chassis._led:
            from .led import SystemLed
            Chassis._led = SystemLed()

    @utils.pre_initialize(initizalize_system_led)
    def set_status_led(self, color):
        """
        Sets the state of the system LED

        Args:
            color: A string representing the color with which to set the
                   system LED

        Returns:
            bool: True if system LED state is set successfully, False if not
        """
        return False if not Chassis._led else Chassis._led.set_status(color)

    @utils.pre_initialize(initizalize_system_led)
    def get_status_led(self):
        """
        Gets the state of the system LED

        Returns:
            A string, one of the valid LED color strings which could be vendor
            specified.
        """
        return None if not Chassis._led else Chassis._led.get_status()

    def get_watchdog(self):
        """
        Retrieves hardware watchdog device on this chassis

        Returns:
            An object derived from WatchdogBase representing the hardware
            watchdog device

        Note:
            We overload this method to ensure that watchdog is only initialized
            when it is referenced. Currently, only one daemon can open the watchdog.
            To initialize watchdog in the constructor causes multiple daemon 
            try opening watchdog when loading and constructing a chassis object
            and fail. By doing so we can eliminate that risk.
        """
        try:
            if self._watchdog is None:
                from .watchdog import get_watchdog
                self._watchdog = get_watchdog()
        except Exception as e:
            logger.log_info("Fail to load watchdog due to {}".format(repr(e)))

        return self._watchdog

    
    def get_revision(self):
        """
        Retrieves the hardware revision of the device
        
        Returns:
            string: Revision value of device
        """
        if self.dmi_data is None:
            self.dmi_data = self._parse_dmi(DMI_FILE)

        return self.dmi_data.get(DMI_VERSION, "N/A")

    def _parse_dmi(self, filename):
        """
        Read DMI data chassis data and returns a dictionary of values

        Returns:
            A dictionary containing the dmi table of the switch chassis info
        """
        result = {}
        try:
            with open(filename, "rb") as fileobj:
                data = fileobj.read()

            body = data[DMI_HEADER_LEN:]
            records = body.split(b'\x00')

            for k, v in DMI_TABLE_MAP.items():
                result[k] = records[v].decode("utf-8")

        except Exception as e:
            logger.log_error("Fail to decode DMI {} due to {}".format(filename, repr(e)))

        return result

    def _verify_reboot_cause(self, filename):
        '''
        Open and read the reboot cause file in 
        /var/run/hwmanagement/system (which is defined as REBOOT_CAUSE_ROOT)
        If a reboot cause file doesn't exists, returns '0'.
        '''
        return bool(utils.read_int_from_file(os.path.join(REBOOT_CAUSE_ROOT, filename)))

    def initialize_reboot_cause(self):
        self.reboot_major_cause_dict = {
            'reset_main_pwr_fail'       :   self.REBOOT_CAUSE_POWER_LOSS,
            'reset_aux_pwr_or_ref'      :   self.REBOOT_CAUSE_POWER_LOSS,
            'reset_asic_thermal'        :   self.REBOOT_CAUSE_THERMAL_OVERLOAD_ASIC,
            'reset_hotswap_or_wd'       :   self.REBOOT_CAUSE_WATCHDOG,
            'reset_swb_wd'              :   self.REBOOT_CAUSE_WATCHDOG,
            'reset_sff_wd'              :   self.REBOOT_CAUSE_WATCHDOG
        }
        self.reboot_minor_cause_dict = {
            'reset_fw_reset'            :   "Reset by ASIC firmware",
            'reset_long_pb'             :   "Reset by long press on power button",
            'reset_short_pb'            :   "Reset by short press on power button",
            'reset_comex_thermal'       :   "ComEx thermal shutdown",
            'reset_comex_pwr_fail'      :   "ComEx power fail",
            'reset_comex_wd'            :   "Reset requested from ComEx",
            'reset_from_asic'           :   "Reset requested from ASIC",
            'reset_reload_bios'         :   "Reset caused by BIOS reload",
            'reset_hotswap_or_halt'     :   "Reset caused by hotswap or halt",
            'reset_from_comex'          :   "Reset from ComEx",
            'reset_voltmon_upgrade_fail':   "Reset due to voltage monitor devices upgrade failure"
        }
        self.reboot_by_software = 'reset_sw_reset'
        self.reboot_cause_initialized = True

    def get_reboot_cause(self):
        """
        Retrieves the cause of the previous reboot

        Returns:
            A tuple (string, string) where the first element is a string
            containing the cause of the previous reboot. This string must be
            one of the predefined strings in this class. If the first string
            is "REBOOT_CAUSE_HARDWARE_OTHER", the second string can be used
            to pass a description of the reboot cause.
        """
        #read reboot causes files in the following order
        if not self.reboot_cause_initialized:
            self.initialize_reboot_cause()

        for reset_file, reset_cause in self.reboot_major_cause_dict.items():
            if self._verify_reboot_cause(reset_file):
                return reset_cause, ''

        for reset_file, reset_cause in self.reboot_minor_cause_dict.items():
            if self._verify_reboot_cause(reset_file):
                return self.REBOOT_CAUSE_HARDWARE_OTHER, reset_cause

        if self._verify_reboot_cause(self.reboot_by_software):
            logger.log_info("Hardware reboot cause: the system was rebooted due to software requesting")
        else:
            logger.log_info("Hardware reboot cause: no hardware reboot cause found")

        return self.REBOOT_CAUSE_NON_HARDWARE, ''

    def get_thermal_manager(self):
        from .thermal_manager import ThermalManager
        return ThermalManager

    def get_position_in_parent(self):
        """
		Retrieves 1-based relative physical position in parent device. If the agent cannot determine the parent-relative position
        for some reason, or if the associated value of entPhysicalContainedIn is '0', then the value '-1' is returned
		Returns:
		    integer: The 1-based relative physical position in parent device or -1 if cannot determine the position
		"""
        return -1

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False


class ModularChassis(Chassis):
    def __init__(self):
        super(ModularChassis, self).__init__()
        self.module_initialized_count = 0

    ##############################################
    # Module methods
    ##############################################
    def initialize_single_module(self, index):
        count = self.get_num_modules()
        if index < count:
            if not self._module_list:
                self._module_list = [None] * count
            
            if not self._module_list[index]:
                from .module import Module
                self._module_list[index] = Module(index + 1)
                self.module_initialized_count += 1

    def initialize_modules(self):
        if not self._module_list:
            from .module import Module
            count = self.get_num_modules()
            for index in range(1, count + 1):
                self._module_list.append(Module(index))
            self.module_initialized_count = count
        elif self.module_initialized_count != len(self._module_list):
            from .module import Module
            for index in range(len(self._module_list)):
                if self._module_list[index] is None:
                    self._module_list[index] = Module(index + 1)
            self.module_initialized_count = len(self._module_list)

    def get_num_modules(self):
        """
        Retrieves the number of modules available on this chassis

        Returns:
            An integer, the number of modules available on this chassis
        """
        return DeviceDataManager.get_linecard_count()

    @utils.pre_initialize(initialize_modules)
    def get_all_modules(self):
        """
        Retrieves all modules available on this chassis

        Returns:
            A list of objects derived from ModuleBase representing all
            modules available on this chassis
        """
        return self._module_list

    @utils.pre_initialize_one(initialize_single_module)
    def get_module(self, index):
        """
        Retrieves module represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the module to
            retrieve

        Returns:
            An object dervied from ModuleBase representing the specified
            module
        """
        module = None

        try:
            module = self._module_list[index]
        except IndexError:
            sys.stderr.write("Module index {} out of range (0-{})\n".format(
                             index, len(self._module_list)-1))

        return module

    ##############################################
    # SFP methods
    ##############################################

    def get_num_sfps(self):
        """
        Retrieves the number of sfps available on this chassis

        Returns:
            An integer, the number of sfps available on this chassis
        """
        return reduce(lambda x, y: x + y, (x.get_num_sfps() for x in self.get_all_modules()))

    def get_all_sfps(self):
        """
        Retrieves all sfps available on this chassis

        Returns:
            A list of objects derived from SfpBase representing all sfps
            available on this chassis
        """
        return reduce(lambda x, y: x + y, (x.get_all_sfps() for x in self.get_all_modules()))

    def get_sfp(self, index):
        """
        Retrieves sfp represented by (1-based) index <index>

        Args:
            index: An integer, the index (1-based) of the sfp to retrieve.
                   The index should be the sequence of a physical port in a chassis,
                   starting from 1.
                   For example, 1 for Ethernet0, 2 for Ethernet4 and so on.

        Returns:
            An object dervied from SfpBase representing the specified sfp
        """
        slot_id = (index & 0xFFFF0000) >> 16 # TODO: align with final design
        module = self.get_module(slot_id - 1)
        if not module:
            return None

        sfp_index = (index & 0x0000FFFF)
        return module.get_sfp(sfp_index - 1)
