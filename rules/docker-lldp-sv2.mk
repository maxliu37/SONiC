# docker image for lldp agent

DOCKER_LLDP_SV2_STEM = docker-lldp-sv2
DOCKER_LLDP_SV2 = $(DOCKER_LLDP_SV2_STEM).gz
DOCKER_LLDP_SV2_DBG = $(DOCKER_LLDP_SV2_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_LLDP_SV2)_PATH = $(DOCKERS_PATH)/docker-lldp-sv2

$(DOCKER_LLDP_SV2)_DEPENDS += $(LLDPD) $(LIBSWSSCOMMON) $(PYTHON_SWSSCOMMON)

$(DOCKER_LLDP_SV2)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_STRETCH)_DBG_DEPENDS)
$(DOCKER_LLDP_SV2)_DBG_DEPENDS += $(LLDPD_DBG) $(LIBSWSSCOMMON_DBG)

$(DOCKER_LLDP_SV2)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_STRETCH)_DBG_IMAGE_PACKAGES)

$(DOCKER_LLDP_SV2)_PYTHON_WHEELS += $(DBSYNCD_PY2)
$(DOCKER_LLDP_SV2)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_STRETCH)

SONIC_DOCKER_IMAGES += $(DOCKER_LLDP_SV2)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_LLDP_SV2)
SONIC_STRETCH_DOCKERS += $(DOCKER_LLDP_SV2)

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_LLDP_SV2_DBG)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_LLDP_SV2_DBG)
SONIC_STRETCH_DBG_DOCKERS += $(DOCKER_LLDP_SV2_DBG)

$(DOCKER_LLDP_SV2)_CONTAINER_NAME = lldp
$(DOCKER_LLDP_SV2)_RUN_OPT += --privileged -t
$(DOCKER_LLDP_SV2)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro

$(DOCKER_LLDP_SV2)_BASE_IMAGE_FILES += lldpctl:/usr/bin/lldpctl
$(DOCKER_LLDP_SV2)_BASE_IMAGE_FILES += lldpcli:/usr/bin/lldpcli
$(DOCKER_LLDP_SV2)_BASE_IMAGE_FILES += monit_lldp:/etc/monit/conf.d
$(DOCKER_LLDP_SV2)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)
