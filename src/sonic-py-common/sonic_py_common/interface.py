"""
 Dictionary of SONIC interface name prefixes. Each entry in the format
 "Human readable interface string":"Sonic interface prefix"
 Currently this is a static mapping, but in future could be stored as metadata in DB.
"""

SONIC_INTERFACE_PREFIXES = {
  "Ethernet-FrontPanel":"Ethernet",
  "PortChannel":"PortChannel",
  "Vlan":"Vlan",
  "Loopback":"Loopback",
  "Ethernet-Backplane":"Ethernet-BP"
}

def fp_interface_prefix():
    """
    Retrieves the SONIC front panel interface name prefix.
    """
    return SONIC_INTERFACE_PREFIXES["Ethernet-FrontPanel"]

def bp_interface_prefix():
    """
    Retrieves the SONIC backplane interface name prefix.
    """
    return SONIC_INTERFACE_PREFIXES["Ethernet-Backplane"]

def portchannel_interface_prefix():
    """
    Retrieves the SONIC PortChannel interface name prefix.
    """
    return SONIC_INTERFACE_PREFIXES["PortChannel"]

def vlan_interface_prefix():
    """
    Retrieves the SONIC Vlan interface name prefix.
    """
    return SONIC_INTERFACE_PREFIXES["Vlan"]

def lo_interface_prefix():
    """
    Retrieves the SONIC Loopback interface name prefix.
    """
    return SONIC_INTERFACE_PREFIXES["Loopback"]
