#!/usr/bin/env python

########################################################################
# DELLEMC N3248TE
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Components' (e.g., BIOS, CPLD, FPGA, BMC etc.) available in
# the platform
#
########################################################################

try:
    import subprocess
    from sonic_platform_base.component_base import ComponentBase

except ImportError as e:
    raise ImportError(str(e) + "- required module not found")
def get_bios_version():
    return subprocess.check_output(['dmidecode', '-s', 'system-version']).strip().decode()

def get_cpld_version(cpld):
    mjr_ver=subprocess.check_output('cat /sys/devices/platform/dell-n3248te-cpld.0/' + cpld + '_mjr_ver', shell=True).strip()[2:].decode()
    mnr_ver=subprocess.check_output('cat /sys/devices/platform/dell-n3248te-cpld.0/' + cpld + '_mnr_ver', shell=True).strip()[2:].decode()
    return (str(mjr_ver) + '.' + str(mnr_ver))

class Component(ComponentBase):
    """DellEMC Platform-specific Component class"""

    CHASSIS_COMPONENTS = [
        ['BIOS',
         'Performs initialization of hardware components during booting',
         get_bios_version()
        ],
        ['CPU CPLD',
         'Used for managing the CPU power sequence and CPU states',
         get_cpld_version('cpu_cpld')
        ],
        ['SYS CPLD',
         'Used for managing FAN, PSU, SFP modules (1-48) SFP Plus modules (49-62)',
         get_cpld_version('sys_cpld')
        ]
    ]

    def __init__(self, component_index=0):
        self.index = component_index
        self.name = self.CHASSIS_COMPONENTS[self.index][0]
        self.description = self.CHASSIS_COMPONENTS[self.index][1]
        self.version = self.CHASSIS_COMPONENTS[self.index][2]

    def get_name(self):
        """
        Retrieves the name of the component
        Returns:
        A string containing the name of the component
        """
        return self.name

    def get_description(self):
        """
        Retrieves the description of the component
        Returns:
        A string containing the description of the component
        """
        return self.description

    def get_firmware_version(self):
        """
        Retrieves the firmware version of the component
        Returns:
            A string containing the firmware version of the component
        """
        return self.version

    def install_firmware(self, image_path):
        """
        Installs firmware to the component
        Args:
        image_path: A string, path to firmware image
        Returns:
        A boolean, True if install was successful, False if not
        """
        return False
