# docker image for any platform syncd with rpc

DOCKER_SYNCD_BASE = docker-syncd-$(DOCKER_SYNCD_PLATFORM_CODE).gz
DOCKER_SYNCD_BASE_RPC = docker-syncd-$(DOCKER_SYNCD_PLATFORM_CODE)-rpc.gz
$(DOCKER_SYNCD_BASE_RPC)_PATH = $(PLATFORM_PATH)/docker-syncd-$(DOCKER_SYNCD_PLATFORM_CODE)-rpc
$(DOCKER_SYNCD_BASE_RPC)_DEPENDS += $(SYNCD_RPC) $(LIBTHRIFT)
$(DOCKER_SYNCD_BASE_RPC)_LOAD_DOCKERS += $(DOCKER_SYNCD_BASE)
SONIC_DOCKER_IMAGES += $(DOCKER_SYNCD_BASE_RPC)
ifeq ($(ENABLE_SYNCD_RPC),y)
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_SYNCD_BASE_RPC)
endif

$(DOCKER_SYNCD_BASE_RPC)_CONTAINER_NAME = syncd
$(DOCKER_SYNCD_BASE_RPC)_RUN_OPT += --net=host --privileged -t
$(DOCKER_SYNCD_BASE_RPC)_RUN_OPT += -v /host/machine.conf:/etc/machine.conf
$(DOCKER_SYNCD_BASE_RPC)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
