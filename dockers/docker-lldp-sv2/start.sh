#!/usr/bin/env bash

dpkg-reconfigure -f noninteractive tzdata

sonic-cfggen -d -t /usr/share/sonic/templates/lldpd.conf.j2 > /etc/lldpd.conf

mkdir -p /var/sonic
echo "# Config files managed by sonic-config-engine" > /var/sonic/config_status

rm -f /var/run/rsyslogd.pid

supervisorctl start rsyslogd
supervisorctl start lldpd
supervisorctl start lldp-syncd
supervisorctl start lldpmgrd
