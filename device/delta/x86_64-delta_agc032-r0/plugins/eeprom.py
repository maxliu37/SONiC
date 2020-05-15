#!/usr/bin/env python

try:
    import exceptions
    import binascii
    import time
    import optparse
    import warnings
    import os
    import sys
    from sonic_eeprom import eeprom_base
    from sonic_eeprom import eeprom_tlvinfo
    import subprocess
except ImportError, e:
    raise ImportError (str(e) + "- required module not found")

class board(eeprom_tlvinfo.TlvInfoDecoder):
    _TLV_INFO_MAX_LEN = 256
    def __init__(self, name, path, cpld_root, ro):
	self.eeprom_path = "/sys/devices/pci0000:00/0000:00:1f.3/i2c-0/0-0053/eeprom"
	super(board, self).__init__(self.eeprom_path, 0, '', True)
