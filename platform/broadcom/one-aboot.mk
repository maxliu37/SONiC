# sonic broadcom one image installer

SONIC_ONE_ABOOT_IMAGE = sonic-aboot-broadcom.swi
$(SONIC_ONE_ABOOT_IMAGE)_MACHINE = broadcom
$(SONIC_ONE_ABOOT_IMAGE)_IMAGE_TYPE = aboot
$(SONIC_ONE_ABOOT_IMAGE)_INSTALLS += $(BRCM_OPENNSL_KERNEL) $(ARISTA_PLATFORM_MODULE_DRIVERS) $(ARISTA_PLATFORM_MODULE_PYTHON2) $(ARISTA_PLATFORM_MODULE_PYTHON3) $(ARISTA_PLATFORM_MODULE)
$(SONIC_ONE_ABOOT_IMAGE)_INSTALLS += $(PHY_CREDO)
$(SONIC_ONE_ABOOT_IMAGE)_INSTALLS += $(SYSTEMD_SONIC_GENERATOR)
$(SONIC_ONE_ABOOT_IMAGE)_LAZY_COMMON_INSTALLS += $(BRCM_DNX_OPENNSL_KERNEL)
ifeq ($(INSTALL_DEBUG_TOOLS),y)
$(SONIC_ONE_ABOOT_IMAGE)_DOCKERS += $(SONIC_INSTALL_DOCKER_DBG_IMAGES)
$(SONIC_ONE_ABOOT_IMAGE)_DOCKERS += $(filter-out $(patsubst %-$(DBG_IMAGE_MARK).gz,%.gz, $(SONIC_INSTALL_DOCKER_DBG_IMAGES)), $(SONIC_INSTALL_DOCKER_IMAGES))
else
$(SONIC_ONE_ABOOT_IMAGE)_DOCKERS += $(SONIC_INSTALL_DOCKER_IMAGES)
endif
SONIC_INSTALLERS += $(SONIC_ONE_ABOOT_IMAGE)
