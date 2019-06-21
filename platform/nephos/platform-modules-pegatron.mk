# Pegatron Platform modules

PEGATRON_PORSCHE_PLATFORM_MODULE_VERSION = 0.0.1
PEGATRON_FN_6254_DN_F_PLATFORM_MODULE_VERSION = 1.0.0

export PEGATRON_PORSCHE_PLATFORM_MODULE_VERSION
export PEGATRON_FN_6254_DN_F_PLATFORM_MODULE_VERSION

PEGATRON_PORSCHE_PLATFORM_MODULE = sonic-platform-pegatron-porsche_$(PEGATRON_PORSCHE_PLATFORM_MODULE_VERSION)_amd64.deb
$(PEGATRON_PORSCHE_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-pegatron
$(PEGATRON_PORSCHE_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(PEGATRON_PORSCHE_PLATFORM_MODULE)_PLATFORM = x86_64-pegatron_porsche-r0
SONIC_DPKG_DEBS += $(PEGATRON_PORSCHE_PLATFORM_MODULE)
SONIC_STRETCH_DEBS += $(PEGATRON_PORSCHE_PLATFORM_MODULE)

PEGATRON_FN_6254_DN_F_PLATFORM_MODULE = sonic-platform-pegatron-fn-6254-dn-f_$(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE_VERSION)_amd64.deb
$(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-pegatron
$(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE)_PLATFORM = x86_64-pegatron_fn_6254_dn_f-r0
SONIC_DPKG_DEBS += $(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE)
SONIC_STRETCH_DEBS += $(PEGATRON_FN_6254_DN_F_PLATFORM_MODULE)

