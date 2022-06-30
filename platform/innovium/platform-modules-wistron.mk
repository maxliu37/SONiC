# Wistron Platform modules

WISTRON_PLATFORM_MODULE_VERSION = 1.1

export WISTRON_PLATFORM_MODULE_VERSION

WISTRON_PLATFORM_MODULE = sonic-platform-wistron-sw-to3200k_$(WISTRON_PLATFORM_MODULE_VERSION)_amd64.deb
$(WISTRON_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-wistron
$(WISTRON_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(WISTRON_PLATFORM_MODULE)_PLATFORM = x86_64-wistron_sw_to3200k-r0

SONIC_DPKG_DEBS += $(WISTRON_PLATFORM_MODULE)
SONIC_STRETCH_DEBS += $(WISTRON_PLATFORM_MODULE)
