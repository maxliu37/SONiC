# linux kernel package

KERNEL_ABI_MINOR_VERSION = 1
KVERSION_SHORT = 4.9.0-7-$(KERNEL_ABI_MINOR_VERSION)
KVERSION = $(KVERSION_SHORT)-amd64
KERNEL_VERSION = 4.9.110
KERNEL_SUBVERSION = 3+deb9u2

export KVERSION_SHORT KVERSION KERNEL_VERSION KERNEL_SUBVERSION

LINUX_HEADERS_COMMON = linux-headers-$(KVERSION_SHORT)-common_$(KERNEL_VERSION)-$(KERNEL_SUBVERSION)_all.deb
$(LINUX_HEADERS_COMMON)_SRC_PATH = $(SRC_PATH)/sonic-linux-kernel
SONIC_MAKE_DEBS += $(LINUX_HEADERS_COMMON)

LINUX_HEADERS = linux-headers-$(KVERSION)_$(KERNEL_VERSION)-$(KERNEL_SUBVERSION)_amd64.deb
$(eval $(call add_derived_package,$(LINUX_HEADERS_COMMON),$(LINUX_HEADERS)))

LINUX_KERNEL = linux-image-$(KVERSION)_$(KERNEL_VERSION)-$(KERNEL_SUBVERSION)_amd64.deb
$(eval $(call add_derived_package,$(LINUX_HEADERS_COMMON),$(LINUX_KERNEL)))
