# pcimem package 

SONIC_PCIMEM_VERSION = 1.0.0
SONIC_PCIMEM_PKG_NAME = pcimem

SONIC_PCIMEM = $(SONIC_PCIMEM_PKG_NAME)_$(SONIC_PCIMEM_VERSION)_$(CONFIGURED_ARCH).deb
$(SONIC_PCIMEM)_SRC_PATH = $(SRC_PATH)/$(SONIC_PCIMEM_PKG_NAME)
SONIC_DPKG_DEBS += $(SONIC_PCIMEM)
