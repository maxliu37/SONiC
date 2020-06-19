# Alphanetworks Platform modules

ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE_VERSION = 1.0
ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE_VERSION = 1.0
ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE_VERSION = 1.0

export ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE_VERSION
export ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE_VERSION
export ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE_VERSION

ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE = sonic-platform-alphanetworks-snh60a0-320fv2_$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE_VERSION)_amd64.deb
$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-alphanetworks
$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE)_PLATFORM = x86_64-alphanetworks_snh60a0_320fv2-r0
SONIC_DPKG_DEBS += $(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE)

ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE = sonic-platform-alphanetworks-snh60b0-640f_$(ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE_VERSION)_amd64.deb
$(ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE)_PLATFORM = x86_64-alphanetworks_snh60b0_640f-r0
$(eval $(call add_extra_package,$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE),$(ALPHANETWORKS_SNH60B0_640F_PLATFORM_MODULE)))

ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE = sonic-platform-alphanetworks-snj60b0-320f_$(ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE_VERSION)_amd64.deb
$(ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE)_PLATFORM = x86_64-alphanetworks_snj60b0_320f-r0
$(eval $(call add_extra_package,$(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE),$(ALPHANETWORKS_SNJ60B0_320F_PLATFORM_MODULE)))

SONIC_STRETCH_DEBS += $(ALPHANETWORKS_SNH60A0_320FV2_PLATFORM_MODULE)


