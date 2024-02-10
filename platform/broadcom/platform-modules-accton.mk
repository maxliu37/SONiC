# Accton Platform modules

ACCTON_AS7712_32X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS5712_54X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7816_64X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7716_32X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7312_54X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7326_56X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7716_32XB_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS6712_32X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7726_32X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS4630_54PE_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS4630_54TE_PLATFORM_MODULE_VERSION = 1.1
ACCTON_MINIPACK_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS5812_54X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS5812_54T_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS5835_54X_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS9716_32D_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS9726_32D_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS5835_54T_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7312_54XS_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7315_27XB_PLATFORM_MODULE_VERSION = 1.1
ACCTON_AS7926_40XFB_PLATFORM_MODULE_VERSION = 1.1

export ACCTON_AS7712_32X_PLATFORM_MODULE_VERSION
export ACCTON_AS5712_54X_PLATFORM_MODULE_VERSION
export ACCTON_AS7816_64X_PLATFORM_MODULE_VERSION
export ACCTON_AS7716_32X_PLATFORM_MODULE_VERSION
export ACCTON_AS7312_54X_PLATFORM_MODULE_VERSION
export ACCTON_AS7326_56X_PLATFORM_MODULE_VERSION
export ACCTON_AS7716_32XB_PLATFORM_MODULE_VERSION
export ACCTON_AS6712_32X_PLATFORM_MODULE_VERSION
export ACCTON_AS7726_32X_PLATFORM_MODULE_VERSION
export ACCTON_AS4630_54PE_PLATFORM_MODULE_VERSION
export ACCTON_AS4630_54TE_PLATFORM_MODULE_VERSION
export ACCTON_MINIPACK_PLATFORM_MODULE_VERSION
export ACCTON_AS5812_54X_PLATFORM_MODULE_VERSION
export ACCTON_AS5812_54T_PLATFORM_MODULE_VERSION
export ACCTON_AS5835_54X_PLATFORM_MODULE_VERSION
export ACCTON_AS9716_32D_PLATFORM_MODULE_VERSION
export ACCTON_AS9726_32D_PLATFORM_MODULE_VERSION
export ACCTON_AS5835_54T_PLATFORM_MODULE_VERSION
export ACCTON_AS7312_54XS_PLATFORM_MODULE_VERSION
export ACCTON_AS7315_27XB_PLATFORM_MODULE_VERSION
export ACCTON_AS7926_40XFB_PLATFORM_MODULE_VERSION

ACCTON_AS7712_32X_PLATFORM_MODULE = sonic-platform-accton-as7712-32x_$(ACCTON_AS7712_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7712_32X_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-accton
$(ACCTON_AS7712_32X_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON) $(PDDF_PLATFORM_MODULE_SYM)
$(ACCTON_AS7712_32X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7712_32x-r0
SONIC_DPKG_DEBS += $(ACCTON_AS7712_32X_PLATFORM_MODULE)

ACCTON_AS5712_54X_PLATFORM_MODULE = sonic-platform-accton-as5712-54x_$(ACCTON_AS5712_54X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS5712_54X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as5712_54x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS5712_54X_PLATFORM_MODULE)))

ACCTON_AS7816_64X_PLATFORM_MODULE = sonic-platform-accton-as7816-64x_$(ACCTON_AS7816_64X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7816_64X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7816_64x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7816_64X_PLATFORM_MODULE)))

ACCTON_AS7716_32X_PLATFORM_MODULE = sonic-platform-accton-as7716-32x_$(ACCTON_AS7716_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7716_32X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7716_32x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7716_32X_PLATFORM_MODULE)))

ACCTON_AS7312_54X_PLATFORM_MODULE = sonic-platform-accton-as7312-54x_$(ACCTON_AS7312_54X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7312_54X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7312_54x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7312_54X_PLATFORM_MODULE)))

ACCTON_AS7312_54XS_PLATFORM_MODULE = sonic-platform-accton-as7312-54xs_$(ACCTON_AS7312_54XS_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7312_54XS_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7312_54xs-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7312_54XS_PLATFORM_MODULE)))

ACCTON_AS7326_56X_PLATFORM_MODULE = sonic-platform-accton-as7326-56x_$(ACCTON_AS7326_56X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7326_56X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7326_56x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7326_56X_PLATFORM_MODULE)))

ACCTON_AS7716_32XB_PLATFORM_MODULE = sonic-platform-accton-as7716-32xb_$(ACCTON_AS7716_32XB_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7716_32XB_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7716_32xb-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7716_32XB_PLATFORM_MODULE)))

ACCTON_AS6712_32X_PLATFORM_MODULE = sonic-platform-accton-as6712-32x_$(ACCTON_AS6712_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS6712_32X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as6712_32x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS6712_32X_PLATFORM_MODULE)))

ACCTON_AS7726_32X_PLATFORM_MODULE = sonic-platform-accton-as7726-32x_$(ACCTON_AS7726_32X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7726_32X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7726_32x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7726_32X_PLATFORM_MODULE)))

ACCTON_AS4630_54PE_PLATFORM_MODULE = sonic-platform-accton-as4630-54pe_$(ACCTON_AS4630_54PE_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS4630_54PE_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as4630_54pe-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS4630_54PE_PLATFORM_MODULE)))

ACCTON_AS4630_54TE_PLATFORM_MODULE = sonic-platform-accton-as4630-54te_$(ACCTON_AS4630_54TE_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS4630_54TE_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as4630_54te-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS4630_54TE_PLATFORM_MODULE)))

ACCTON_MINIPACK_PLATFORM_MODULE = sonic-platform-accton-minipack_$(ACCTON_MINIPACK_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_MINIPACK_PLATFORM_MODULE)_PLATFORM = x86_64-accton_minipack-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_MINIPACK_PLATFORM_MODULE)))

ACCTON_AS5812_54X_PLATFORM_MODULE = sonic-platform-accton-as5812-54x_$(ACCTON_AS5812_54X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS5812_54X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as5812_54x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS5812_54X_PLATFORM_MODULE)))

ACCTON_AS5812_54T_PLATFORM_MODULE = sonic-platform-accton-as5812-54t_$(ACCTON_AS5812_54T_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS5812_54T_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as5812_54t-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS5812_54T_PLATFORM_MODULE)))

ACCTON_AS5835_54X_PLATFORM_MODULE = sonic-platform-accton-as5835-54x_$(ACCTON_AS5835_54X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS5835_54X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as5835_54x-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS5835_54X_PLATFORM_MODULE)))

ACCTON_AS9716_32D_PLATFORM_MODULE = sonic-platform-accton-as9716-32d_$(ACCTON_AS9716_32D_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS9716_32D_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as9716_32d-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS9716_32D_PLATFORM_MODULE)))

ACCTON_AS9726_32D_PLATFORM_MODULE = sonic-platform-accton-as9726-32d_$(ACCTON_AS9726_32D_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS9726_32D_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as9726_32d-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS9726_32D_PLATFORM_MODULE)))

ACCTON_AS5835_54T_PLATFORM_MODULE = sonic-platform-accton-as5835-54t_$(ACCTON_AS5835_54T_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS5835_54T_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as5835_54t-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS5835_54T_PLATFORM_MODULE)))

ACCTON_AS7315_27XB_PLATFORM_MODULE = sonic-platform-accton-as7315-27xb_$(ACCTON_AS7315_27XB_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7315_27XB_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7315_27xb-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7315_27XB_PLATFORM_MODULE)))

ACCTON_AS7926_40XFB_PLATFORM_MODULE = sonic-platform-accton-as7926-40xfb_$(ACCTON_AS7926_40XFB_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_AS7926_40XFB_PLATFORM_MODULE)_PLATFORM = x86_64-accton_as7926_40xfb-r0
$(eval $(call add_extra_package,$(ACCTON_AS7712_32X_PLATFORM_MODULE),$(ACCTON_AS7926_40XFB_PLATFORM_MODULE)))
