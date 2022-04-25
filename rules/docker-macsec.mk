# docker image for macsec agent

DOCKER_MACSEC_STEM = docker-macsec
DOCKER_MACSEC = $(DOCKER_MACSEC_STEM).gz
DOCKER_MACSEC_DBG = $(DOCKER_MACSEC_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_MACSEC)_PATH = $(DOCKERS_PATH)/$(DOCKER_MACSEC_STEM)

$(DOCKER_MACSEC)_DEPENDS += $(SWSS) $(WPASUPPLICANT) $(LIBSWSSCOMMON) $(LIBNL3) $(LIBNL_GENL3) $(LIBNL_ROUTE3)
$(DOCKER_MACSEC)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_DEPENDS)
$(DOCKER_MACSEC)_DBG_DEPENDS += $(SWSS_DBG) $(WPASUPPLICANT_DBG) $(LIBSWSSCOMMON_DBG)

$(DOCKER_MACSEC)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_IMAGE_PACKAGES)

$(DOCKER_MACSEC)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_BULLSEYE)

$(DOCKER_MACSEC)_INSTALL_PYTHON_WHEELS = $(SONIC_UTILITIES_PY3)
$(DOCKER_MACSEC)_INSTALL_DEBS = $(PYTHON3_SWSSCOMMON) $(LIBYANG_PY3)

SONIC_DOCKER_IMAGES += $(DOCKER_MACSEC)
# ifeq ($(INCLUDE_MACSEC), y)
# SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_MACSEC)
# endif

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_MACSEC_DBG)
# ifeq ($(INCLUDE_MACSEC), y)
# SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_MACSEC_DBG)
# endif

ifeq ($(INCLUDE_MACSEC),y)
ifeq ($(INSTALL_DEBUG_TOOLS),y)
SONIC_PACKAGES_LOCAL += $(DOCKER_MACSEC_DBG)
else
SONIC_PACKAGES_LOCAL += $(DOCKER_MACSEC)
endif
endif

$(DOCKER_MACSEC)_CONTAINER_NAME = macsec
$(DOCKER_MACSEC)_VERSION = 1.0.0
$(DOCKER_MACSEC)_PACKAGE_NAME = macsec
$(DOCKER_MACSEC)_RUN_OPT += --privileged -t
$(DOCKER_MACSEC)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_MACSEC)_RUN_OPT += -v /host/warmboot:/var/warmboot

$(DOCKER_MACSEC)_CLI_CONFIG_PLUGIN = /cli/config/plugins/macsec.py

# $(DOCKER_MACSEC)_CLI_SHOW_PLUGIN = /cli/show/plugins/show_dhcp_relay.py

$(DOCKER_MACSEC)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)

SONIC_BULLSEYE_DOCKERS += $(DOCKER_MACSEC)
SONIC_BULLSEYE_DBG_DOCKERS += $(DOCKER_MACSEC_DBG)
