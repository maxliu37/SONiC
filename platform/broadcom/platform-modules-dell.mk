# Dell Z9100 Platform modules

DELL_Z9100_PLATFORM_MODULE_VERSION = 1.1

export DELL_Z9100_PLATFORM_MODULE_VERSION

DELL_Z9100_PLATFORM_MODULE = platform-modules-z9100_$(DELL_Z9100_PLATFORM_MODULE_VERSION)_amd64.deb
$(DELL_Z9100_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-dell
$(DELL_Z9100_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
SONIC_DPKG_DEBS += $(DELL_Z9100_PLATFORM_MODULE)
