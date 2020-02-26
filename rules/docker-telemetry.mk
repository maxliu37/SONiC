# docker image for telemetry agent

DOCKER_TELEMETRY_STEM = docker-sonic-telemetry
DOCKER_TELEMETRY = $(DOCKER_TELEMETRY_STEM).gz
DOCKER_TELEMETRY_DBG = $(DOCKER_TELEMETRY_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_TELEMETRY)_PATH = $(DOCKERS_PATH)/$(DOCKER_TELEMETRY_STEM)

$(DOCKER_TELEMETRY)_DEPENDS += $(REDIS_TOOLS) $(SONIC_TELEMETRY)
$(DOCKER_TELEMETRY)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_STRETCH)_DBG_DEPENDS)

$(DOCKER_TELEMETRY)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_STRETCH)
$(DOCKER_TELEMETRY)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_STRETCH)_DBG_IMAGE_PACKAGES)

SONIC_DOCKER_IMAGES += $(DOCKER_TELEMETRY)
ifeq ($(ENABLE_SYSTEM_TELEMETRY), y)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_TELEMETRY)
SONIC_STRETCH_DOCKERS += $(DOCKER_TELEMETRY)
endif

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_TELEMETRY_DBG)
ifeq ($(ENABLE_SYSTEM_TELEMETRY), y)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_TELEMETRY_DBG)
SONIC_STRETCH_DBG_DOCKERS += $(DOCKER_TELEMETRY_DBG)
endif

$(DOCKER_TELEMETRY)_CONTAINER_NAME = telemetry
$(DOCKER_TELEMETRY)_RUN_OPT += --privileged -t
$(DOCKER_TELEMETRY)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_TELEMETRY)_RUN_OPT += --mount type=bind,source="/var/platform/",target="/mnt/platform/"

ifeq ($(ENABLE_SYSTEM_TELEMETRY), y)
SONIC_OPTIONAL_DOCKER_CONTAINERS += $(DOCKER_TELEMETRY)
endif

$(DOCKER_TELEMETRY)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)
$(DOCKER_TELEMETRY)_BASE_IMAGE_FILES += monit_telemetry:/etc/monit/conf.d
