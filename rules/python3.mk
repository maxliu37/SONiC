# python3.5.2+

PYTHON_VER=3.6.0-1
PYTHON_PNAME=python3.6

export PYTHON_VER
export PYTHON_PNAME

LIBPY3_MIN = lib$(PYTHON_PNAME)-minimal_$(PYTHON_VER)_amd64.deb
$(LIBPY3_MIN)_SRC_PATH = $(SRC_PATH)/python3
$(LIBPY3_MIN)_DEPENDS += 
$(LIBPY3_MIN)_RDEPENDS += 
SONIC_MAKE_DEBS += $(LIBPY3_MIN)

LIBPY3_STD = lib$(PYTHON_PNAME)-stdlib_$(PYTHON_VER)_amd64.deb
$(eval $(call add_derived_package,$(LIBPY3_MIN),$(LIBPY3_STD)))
$(LIBPY3_STD)_DEPENDS += $(LIBMPDECIMAL)
$(LIBPY3_STD)_RDEPENDS += $(LIBPY3_MIN) $(LIBMPDECIMAL)

LIBPY3 = lib$(PYTHON_PNAME)_$(PYTHON_VER)_amd64.deb
$(eval $(call add_derived_package,$(LIBPY3_MIN),$(LIBPY3)))
$(LIBPY3)_DEPENDS += $(LIBPY3_STD)
$(LIBPY3)_RDEPENDS += $(LIBPY3_MIN) $(LIBPY3_STD)

PY3_MIN = $(PYTHON_PNAME)-minimal_$(PYTHON_VER)_amd64.deb
$(eval $(call add_derived_package,$(LIBPY3_MIN),$(PY3_MIN)))
$(PY3_MIN)_RDEPENDS += $(LIBPY3_MIN)

PY3 = $(PYTHON_PNAME)_$(PYTHON_VER)_amd64.deb
$(eval $(call add_derived_package,$(LIBPY3_MIN),$(PY3)))
$(PY3)_DEPENDS += $(PY3_MIN) $(LIBPY3)
$(PY3)_RDEPENDS += $(PY3_MIN) $(LIBPY3) $(LIBPY3_MIN)

LIBPY3_DEV = lib$(PYTHON_PNAME)-dev_$(PYTHON_VER)_amd64.deb
$(eval $(call add_derived_package,$(LIBPY3_MIN),$(LIBPY3_DEV)))
$(LIBPY3_DEV)_DEPENDS += $(LIBPY3) $($(LIBPY3)_DEPENDS)
$(LIBPY3_DEV)_RDEPENDS += $(LIBPY3) $($(LIBPY3)_RDEPENDS)

