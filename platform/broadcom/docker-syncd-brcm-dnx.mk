# docker image for brcm-dnx syncd

DOCKER_SYNCD_DNX_BASE = docker-syncd-brcm-dnx.gz
DOCKER_SYNCD_DNX_BASE_DBG = docker-syncd-brcm-dnx-$(DBG_IMAGE_MARK).gz
DOCKER_SYNCD_DNX_PLATFORM_CODE = brcm-dnx

$(DOCKER_SYNCD_DNX_BASE)_PATH = $(PLATFORM_PATH)/docker-syncd-$(DOCKER_SYNCD_DNX_PLATFORM_CODE)
$(DOCKER_SYNCD_DNX_BASE)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)

$(DOCKER_SYNCD_DNX_BASE)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_BUSTER)
$(DOCKER_SYNCD_DNX_BASE)_DBG_DEPENDS += $($(DOCKER_CONFIG_ENGINE_BUSTER)_DBG_DEPENDS)
$(DOCKER_SYNCD_DNX_BASE)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_BUSTER)_DBG_IMAGE_PACKAGES)

SONIC_DOCKER_IMAGES += $(DOCKER_SYNCD_DNX_BASE)
ifneq ($(ENABLE_SYNCD_RPC),y)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_SYNCD_DNX_BASE)
endif

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_SYNCD_DNX_BASE_DBG)
ifneq ($(ENABLE_SYNCD_RPC),y)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_SYNCD_DNX_BASE_DBG)
endif


$(DOCKER_SYNCD_DNX_BASE)_DEPENDS += $(SYNCD)
$(DOCKER_SYNCD_DNX_BASE)_DEPENDS += $(BRCM_DNX_SAI)
$(DOCKER_SYNCD_DNX_BASE)_FILES += $(DSSERVE) $(BCMCMD)

ifeq ($(INSTALL_DEBUG_TOOLS), y)
$(DOCKER_SYNCD_DNX_BASE)_DBG_DEPENDS += $(SYNCD_DBG) \
                                $(LIBSWSSCOMMON_DBG) \
                                $(LIBSAIMETADATA_DBG) \
                                $(LIBSAIREDIS_DBG)
endif

$(DOCKER_SYNCD_DNX_BASE)_VERSION = 1.0.0
$(DOCKER_SYNCD_DNX_BASE)_PACKAGE_NAME = syncd-dnx
$(DOCKER_SYNCD_DNX_BASE)_MACHINE = broadcom-dnx
$(DOCKER_SYNCD_DNX_BASE)_AFTER = $(DOCKER_SYNCD_BASE)
$(DOCKER_SYNCD_DNX_BASE)_CONTAINER_NAME = syncd
$(DOCKER_SYNCD_DNX_BASE)_RUN_OPT += --privileged -t
$(DOCKER_SYNCD_DNX_BASE)_RUN_OPT += -v /host/machine.conf:/etc/machine.conf
$(DOCKER_SYNCD_DNX_BASE)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_SYNCD_DNX_BASE)_RUN_OPT += -v /host/warmboot:/var/warmboot

$(DOCKER_SYNCD_DNX_BASE)_BASE_IMAGE_FILES += bcmcmd:/usr/bin/bcmcmd
$(DOCKER_SYNCD_DNX_BASE)_BASE_IMAGE_FILES += bcmsh:/usr/bin/bcmsh
$(DOCKER_SYNCD_DNX_BASE)_BASE_IMAGE_FILES += bcm_common:/usr/bin/bcm_common
