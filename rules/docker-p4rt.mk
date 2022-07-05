# docker image for p4rt

DOCKER_P4RT_STEM = docker-sonic-p4rt
DOCKER_P4RT = $(DOCKER_P4RT_STEM).gz
DOCKER_P4RT_DBG = $(DOCKER_P4RT_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_P4RT)_PATH = $(DOCKERS_PATH)/$(DOCKER_P4RT_STEM)

$(DOCKER_P4RT)_DEPENDS += $(SONIC_P4RT)
$(DOCKER_P4RT)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_DEPENDS)
$(DOCKER_P4RT)_DBG_DEPENDS += $(SONIC_P4RT_DBG) $(LIBSWSSCOMMON_DBG)
$(DOCKER_P4RT)_DBG_DEPENDS += $(LIBSAIREDIS_DBG)
$(DOCKER_P4RT)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_IMAGE_PACKAGES)

$(DOCKER_P4RT)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_BULLSEYE)

$(DOCKER_P4RT)_VERSION = 1.0.0
$(DOCKER_P4RT)_PACKAGE_NAME = p4rt
$(DOCKER_P4RT)_WARM_SHUTDOWN_BEFORE = swss
$(DOCKER_P4RT)_FAST_SHUTDOWN_BEFORE = swss

SONIC_DOCKER_IMAGES += $(DOCKER_P4RT)
SONIC_DOCKER_DBG_IMAGES += $(DOCKER_P4RT_DBG)

ifeq ($(INCLUDE_P4RT), y)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_P4RT)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_P4RT_DBG)
endif

$(DOCKER_P4RT)_CONTAINER_NAME = p4rt
$(DOCKER_P4RT)_RUN_OPT += --privileged -t
$(DOCKER_P4RT)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_P4RT)_GIT_COMMIT = $(shell cd "$($(SONIC_P4RT)_SRC_PATH)" && git log -n 1 --format=format:"%H %s" || echo "Unable to fetch git log for p4rt")

$(DOCKER_P4RT)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)
$(DOCKER_P4RT)_BASE_IMAGE_FILES += monit_p4rt:/etc/monit/conf.d
