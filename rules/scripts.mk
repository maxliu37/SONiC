
ARP_UPDATE_SCRIPT = arp_update
$(ARP_UPDATE_SCRIPT)_PATH = files/scripts

CONFIGDB_LOAD_SCRIPT = configdb-load.sh
$(CONFIGDB_LOAD_SCRIPT)_PATH = files/scripts

BUFFERS_CONFIG_TEMPLATE = buffers_config.j2
$(BUFFERS_CONFIG_TEMPLATE)_PATH = files/build_templates

QOS_CONFIG_TEMPLATE = qos_config.j2
$(QOS_CONFIG_TEMPLATE)_PATH = files/build_templates

SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT = supervisor-proc-exit-listener
$(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)_PATH = files/scripts

SONIC_COPY_FILES += $(CONFIGDB_LOAD_SCRIPT) \
                    $(ARP_UPDATE_SCRIPT) \
                    $(BUFFERS_CONFIG_TEMPLATE) \
                    $(QOS_CONFIG_TEMPLATE) \
                    $(SUPERVISOR_PROC_EXIT_LISTENER_SCRIPT)


