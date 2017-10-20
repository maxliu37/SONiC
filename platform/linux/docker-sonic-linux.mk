# docker image for linux sonic docker image

DOCKER_SONIC_LINUX = docker-sonic-linux.gz
$(DOCKER_SONIC_LINUX)_PATH = $(PLATFORM_PATH)/docker-sonic-linux
$(DOCKER_SONIC_LINUX)_DEPENDS += $(SWSS) $(SYNCD_VS) $(REDIS_SERVER) $(REDIS_TOOLS) $(LIBTEAMDCT) $(LIBTEAM_UTILS) 

ifeq ($(SONIC_ROUTING_STACK), quagga)
$(DOCKER_SONIC_LINUX)_DEPENDS += $(QUAGGA)
else ifeq ($(SONIC_ROUTING_STACK), frr)
$(DOCKER_SONIC_LINUX)_DEPENDS += $(FRR)
else
$(DOCKER_SONIC_LINUX)_DEPENDS += $(GOBGP)
endif

$(DOCKER_SONIC_LINUX)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE)
SONIC_DOCKER_IMAGES += $(DOCKER_SONIC_LINUX)
