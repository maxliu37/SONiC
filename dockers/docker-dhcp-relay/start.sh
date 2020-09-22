#!/usr/bin/env bash

# This version is per docker. To be updated upon updates.
# Hence this could be different from version of other features
IMAGE_VERSION = "1.0.0"

if [ "${RUNTIME_OWNER}" == "" ]; then
    RUNTIME_OWNER="kube"
fi

/usr/share/sonic/scripts/container_state up -f dhcp_relay -o ${RUNTIME_OWNER} -v ${IMAGE_VERSION}

# If our supervisor config has entries in the "isc-dhcp-relay" group...
if [ $(supervisorctl status | grep -c "^isc-dhcp-relay:") -gt 0 ]; then
    # Wait for all interfaces to come up and be assigned IPv4 addresses before
    # starting the DHCP relay agent(s). If an interface the relay should listen
    # on is down, the relay agent will not start. If an interface the relay
    # should listen on is up but does not have an IP address assigned when the
    # relay agent starts, it will not listen or send on that interface for the
    # lifetime of the process.
    /usr/bin/wait_for_intf.sh
fi
