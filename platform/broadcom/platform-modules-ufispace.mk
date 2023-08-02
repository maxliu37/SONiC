# UfiSpace Platform modules

UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION = 1.0.0
UFISPACE_S7801_54XS_PLATFORM_MODULE_VERSION = 1.0.0

export UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION
export UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION
export UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION
export UFISPACE_S7801_54XS_PLATFORM_MODULE_VERSION

UFISPACE_S9300_32D_PLATFORM_MODULE = sonic-platform-ufispace-s9300-32d_$(UFISPACE_S9300_32D_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9300_32D_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-ufispace
$(UFISPACE_S9300_32D_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(UFISPACE_S9300_32D_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9300_32d-r0
SONIC_DPKG_DEBS += $(UFISPACE_S9300_32D_PLATFORM_MODULE)

UFISPACE_S9110_32X_PLATFORM_MODULE = sonic-platform-ufispace-s9110-32x_$(UFISPACE_S9110_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S9110_32X_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s9110_32x-r0
$(eval $(call add_extra_package,$(UFISPACE_S9300_32D_PLATFORM_MODULE),$(UFISPACE_S9110_32X_PLATFORM_MODULE)))

UFISPACE_S8901_54XC_PLATFORM_MODULE = sonic-platform-ufispace-s8901-54xc_$(UFISPACE_S8901_54XC_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S8901_54XC_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s8901_54xc-r0
$(eval $(call add_extra_package,$(UFISPACE_S9300_32D_PLATFORM_MODULE),$(UFISPACE_S8901_54XC_PLATFORM_MODULE)))

UFISPACE_S7801_54XS_PLATFORM_MODULE = sonic-platform-ufispace-s7801-54xs_$(UFISPACE_S7801_54XS_PLATFORM_MODULE_VERSION)_amd64.deb
$(UFISPACE_S7801_54XS_PLATFORM_MODULE)_PLATFORM = x86_64-ufispace_s7801_54xs-r0
$(eval $(call add_extra_package,$(UFISPACE_S9300_32D_PLATFORM_MODULE),$(UFISPACE_S7801_54XS_PLATFORM_MODULE)))

