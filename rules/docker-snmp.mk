# docker image for snmp agent

DOCKER_SNMP_STEM = docker-snmp
DOCKER_SNMP = $(DOCKER_SNMP_STEM).gz
DOCKER_SNMP_DBG = $(DOCKER_SNMP_STEM)-$(DBG_IMAGE_MARK).gz

$(DOCKER_SNMP)_PATH = $(DOCKERS_PATH)/docker-snmp

## TODO: remove LIBPY3_DEV if we can get pip3 directly
$(DOCKER_SNMP)_DEPENDS += $(SNMP) $(SNMPD)

$(DOCKER_SNMP)_DBG_DEPENDS = $($(DOCKER_CONFIG_ENGINE_BUSTER)_DBG_DEPENDS)
$(DOCKER_SNMP)_DBG_DEPENDS += $(SNMP_DBG) $(SNMPD_DBG) $(LIBSNMP_DBG)

$(DOCKER_SNMP)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_BUSTER)_DBG_IMAGE_PACKAGES)

$(DOCKER_SNMP)_PYTHON_WHEELS += $(SONIC_PY_COMMON_PY3) $(SONIC_PLATFORM_COMMON_PY3) $(SWSSSDK_PY3) $(ASYNCSNMP_PY3)
$(DOCKER_SNMP)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_BUSTER)

$(DOCKER_SNMP)_VERSION = 1.0.0
$(DOCKER_SNMP)_PACKAGE_NAME = snmp

SONIC_DOCKER_IMAGES += $(DOCKER_SNMP)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_SNMP)

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_SNMP_DBG)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_SNMP_DBG)

$(DOCKER_SNMP)_CONTAINER_NAME = snmp
$(DOCKER_SNMP)_RUN_OPT += --privileged -t
$(DOCKER_SNMP)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_SNMP)_RUN_OPT += -v /usr/share/sonic/scripts:/usr/share/sonic/scripts:ro
$(DOCKER_SNMP)_FILES += $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)

SONIC_BUSTER_DOCKERS += $(DOCKER_SNMP)
SONIC_BUSTER_DBG_DOCKERS += $(DOCKER_SNMP_DBG)
