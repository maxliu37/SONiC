## RA-B6010-48GT4X
RA_B6010_48GT4X_PLATFORM_MODULE_VERSION =1.3
export RA_B6010_48GT4X_PLATFORM_MODULE_VERSION

RA_B6010_48GT4X_PLATFORM_MODULE = platform-modules-ra-b6010-48gt4x_$(RA_B6010_48GT4X_PLATFORM_MODULE_VERSION)_arm64.deb

$(RA_B6010_48GT4X_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-ragile
$(RA_B6010_48GT4X_PLATFORM_MODULE)_PLATFORM = arm64-ragile_ra-b6010-48gt4x-r0
$(RA_B6010_48GT4X_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
SONIC_DPKG_DEBS += $(RA_B6010_48GT4X_PLATFORM_MODULE)
