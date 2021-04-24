# libpam-radius-auth packages

PAM_RADIUS_VERSION = 1.4.1-1

export PAM_RADIUS_VERSION

LIBPAM_RADIUS = libpam-radius-auth_$(PAM_RADIUS_VERSION)_amd64.deb
$(LIBPAM_RADIUS)_SRC_PATH = $(SRC_PATH)/radius/pam
SONIC_MAKE_DEBS += $(LIBPAM_RADIUS)

SONIC_STRETCH_DEBS += $(LIBPAM_RADIUS)

# libnss-radius packages

NSS_RADIUS_VERSION = 1.0.1-1

export NSS_RADIUS_VERSION

LIBNSS_RADIUS = libnss-radius_$(NSS_RADIUS_VERSION)_amd64.deb
$(LIBNSS_RADIUS)_SRC_PATH = $(SRC_PATH)/radius/nss
SONIC_MAKE_DEBS += $(LIBNSS_RADIUS)

SONIC_STRETCH_DEBS += $(LIBNSS_RADIUS)

