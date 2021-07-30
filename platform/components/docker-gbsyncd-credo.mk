DOCKER_GBSYNCD_PLATFORM_CODE = credo

LIBSAI_CREDO = libsaicredo_0.5.1-alpha.2_amd64.deb
$(LIBSAI_CREDO)_URL =
LIBSAI_CREDO_OWL = libsaicredo-owl_0.5.1-alpha.2_amd64.deb
$(LIBSAI_CREDO_OWL)_URL =

ifneq ($($(LIBSAI_CREDO)_URL),)
include $(PLATFORM_PATH)/../template/docker-gbsyncd-base.mk
$(DOCKER_GBSYNCD_BASE)_PATH = $(PLATFORM_PATH)/../components/docker-gbsyncd-$(DOCKER_GBSYNCD_PLATFORM_CODE)
SONIC_ONLINE_DEBS += $(LIBSAI_CREDO) $(LIBSAI_CREDO_OWL)
$(DOCKER_GBSYNCD_BASE)_DEPENDS += $(SYNCD) $(LIBSAI_CREDO) $(LIBSAI_CREDO_OWL)
endif
