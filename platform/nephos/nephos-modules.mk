# Nephos Platform modules

VERSION = 1.0.0

ifneq ($(NEPHOS_SAI_DEB_LOCAL_URL), )
SDK_FROM_LOCAL = y
else
SDK_FROM_LOCAL = n
endif

SDK_VERSION = 3.0.0
LINUX_VER = 4.9.0-9-2
SDK_COMMIT_ID = 529202

ifeq ($(SAI_FROM_LOCAL), y)
NEPHOS_MODULE = nps-modules-$(LINUX_VER)_$(SDK_VERSION)_$(SDK_COMMIT_ID)_amd64.deb
$(NEPHOS_MODULE)_PATH = $(NEPHOS_SAI_DEB_LOCAL_URL)
SONIC_COPY_DEBS += $(NEPHOS_MODULE)
else
NEPHOS_MODULE = nephos-modules_$(VERSION)_amd64.deb
$(NEPHOS_MODULE)_SRC_PATH = $(PLATFORM_PATH)/nephos-modules
$(NEPHOS_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
SONIC_DPKG_DEBS += $(NEPHOS_MODULE)
endif

SONIC_STRETCH_DEBS += $(NEPHOS_MODULE)
