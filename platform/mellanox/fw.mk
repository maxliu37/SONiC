# mellanox firmware

MLNX_FW_VERSION = 13.2000.1636
MLNX_FW_FILE = fw-SPC-rel-$(subst .,_,$(MLNX_FW_VERSION))-EVB.mfa
$(MLNX_FW_FILE)_URL = $(MLNX_SDK_BASE_URL)/$(MLNX_FW_FILE)
SONIC_ONLINE_FILES += $(MLNX_FW_FILE)

MLNX_SN2700_CPLD_ARCHIVE = msn2700_cpld.tar.gz
$(MLNX_SN2700_CPLD_ARCHIVE)_PATH = platform/mellanox/fw/cpld/
SONIC_COPY_FILES += $(MLNX_SN2700_CPLD_ARCHIVE)

MLNX_CPLD_ARCHIVES += $(MLNX_SN2700_CPLD_ARCHIVE)

export MLNX_FW_VERSION
export MLNX_FW_FILE

export MLNX_SN2700_CPLD_ARCHIVE
export MLNX_CPLD_ARCHIVES
