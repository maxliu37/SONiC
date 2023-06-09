# genl-packet listener package
GENL_PACKET_VERSION = 1.0-1
GENL_PACKET_DIR = sonic-genl-packet

GENL_TOOLS_NAME = genl-packet-tools
GENL_TOOLS = $(GENL_TOOLS_NAME)_$(GENL_PACKET_VERSION)_$(CONFIGURED_ARCH).deb
$(GENL_TOOLS)_SRC_PATH = $(SRC_PATH)/$(GENL_PACKET_DIR)/$(GENL_TOOLS_NAME)/
$(GENL_TOOLS)_VERSION =$(GENL_PACKET_VERSION)
$(GENL_TOOLS)_NAME = $(GENL_TOOLS_NAME)
$(GENL_TOOLS)_DEPENDS += $(LIBNL3_DEV)  $(LIBNL_GENL3_DEV)
$(GENL_TOOLS)_RDEPENDS += $(LIBNL3)  $(LIBNL_GENL3) $(LIBGENL_PACKET)
SONIC_DPKG_DEBS += $(GENL_TOOLS)


