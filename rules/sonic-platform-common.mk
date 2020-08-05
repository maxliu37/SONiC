# sonic-platform-common package

SONIC_PLATFORM_COMMON_PY2 = sonic_platform_common-1.0-py2-none-any.whl
$(SONIC_PLATFORM_COMMON_PY2)_SRC_PATH = $(SRC_PATH)/sonic-platform-common
$(SONIC_PLATFORM_COMMON_PY2)_PYTHON_VERSION = 2
$(SONIC_PLATFORM_COMMON_PY2)_DEPENDS += $(SONIC_PY_COMMON_PY2) $(SONIC_CONFIG_ENGINE)
SONIC_PYTHON_WHEELS += $(SONIC_PLATFORM_COMMON_PY2)

# Als build sonic-platform-common into python3 wheel, so we can use PSU code in SNMP docker
SONIC_PLATFORM_COMMON_PY3 = sonic_platform_common-1.0-py3-none-any.whl
$(SONIC_PLATFORM_COMMON_PY3)_SRC_PATH = $(SRC_PATH)/sonic-platform-common
$(SONIC_PLATFORM_COMMON_PY3)_PYTHON_VERSION = 3
$(SONIC_PLATFORM_COMMON_PY3)_DEPENDS += $(SONIC_PY_COMMON_PY3) $(SONIC_CONFIG_ENGINE)
# Synthetic dependency just to avoid race condition
$(SONIC_PLATFORM_COMMON_PY3)_DEPENDS += $(SONIC_PLATFORM_COMMON_PY2)
$(SONIC_PLATFORM_COMMON_PY3)_TEST = n
# Disable building Python 3 package for now, becuase it currently depends on sonic-config-engine,
# and we're not yet building a Python 3 package for sonic-config-engine
#SONIC_PYTHON_WHEELS += $(SONIC_PLATFORM_COMMON_PY3)
