# docker image for eventd

DOCKER_EVENTD_STEM = docker-eventd
DOCKER_EVENTD = $(DOCKER_EVENTD_STEM).gz
DOCKER_EVENTD_DBG = $(DOCKER_EVENTD_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_EVENTD)_DEPENDS += $(SONIC_EVENTD)

$(DOCKER_EVENTD)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_DEPENDS)
$(DOCKER_EVENTD)_DBG_DEPENDS += $(SONIC_EVENTD_DBG) $(LIBSWSSCOMMON_DBG)

$(DOCKER_EVENTD)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_BULLSEYE)_DBG_IMAGE_PACKAGES)

$(DOCKER_EVENTD)_LOAD_DOCKERS = $(DOCKER_CONFIG_ENGINE_BULLSEYE)

$(DOCKER_EVENTD)_PATH = $(DOCKERS_PATH)/$(DOCKER_EVENTD_STEM)

$(DOCKER_EVENTD)_INSTALL_PYTHON_WHEELS = $(SONIC_UTILITIES_PY3)
$(DOCKER_EVENTD)_INSTALL_DEBS = $(PYTHON3_SWSSCOMMON)

$(DOCKER_EVENTD)_VERSION = 1.0.0
$(DOCKER_EVENTD)_PACKAGE_NAME = eventd

$(DOCKER_DHCP)_SERVICE_REQUIRES = updategraph
$(DOCKER_DHCP)_SERVICE_AFTER = database

SONIC_DOCKER_IMAGES += $(DOCKER_EVENTD)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_EVENTD)

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_EVENTD_DBG)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_EVENTD_DBG)

$(DOCKER_EVENTD)_CONTAINER_NAME = eventd
$(DOCKER_EVENTD)_RUN_OPT += --privileged -t
$(DOCKER_EVENTD)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro

SONIC_BULLSEYE_DOCKERS += $(DOCKER_EVENTD)
SONIC_BULLSEYE_DBG_DOCKERS += $(DOCKER_EVENTD_DBG)

$(DOCKER_EVENTD)_FILESPATH = $($(SONIC_EVENTD)_SRC_PATH)/rsyslog_plugin

$(DOCKER_EVENTD)_PLUGIN = rsyslog_plugin
$($(DOCKER_EVENTD)_PLUGIN)_PATH = $($(DOCKER_EVENTD)_FILESPATH)

SONIC_COPY_FILES += $($(DOCKER_EVENTD)_PLUGIN)

