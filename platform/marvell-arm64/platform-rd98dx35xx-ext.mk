# AC5X External CPU Platform

include $(PLATFORM_PATH)/prestera.mk
AC5X_VERSION=1.0
AC5X_RD98DX35xxEXT_PLATFORM = sonic-platform-rd98dx35xx-ext_$(AC5X_VERSION)_$(CONFIGURED_ARCH).deb
$(AC5X_RD98DX35xxEXT_PLATFORM)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-rd98dx35xx-ext
$(AC5X_RD98DX35xxEXT_PLATFORM)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(AC5X_RD98DX35xxEXT_PLATFORM)_PLATFORM = arm64-marvell_rd98DX35xx_ext-r0
SONIC_DPKG_DEBS += $(AC5X_RD98DX35xxEXT_PLATFORM)

