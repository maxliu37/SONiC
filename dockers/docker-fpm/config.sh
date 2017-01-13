#!/bin/bash

sonic-cfggen -m /etc/sonic/minigraph.xml -t /etc/swss/bgp/bgpd.conf.j2 >/etc/quagga/bgpd.conf
sonic-cfggen -m /etc/sonic/minigraph.xml -t /etc/swss/bgp/zebra.conf.j2 >/etc/quagga/zebra.conf

sonic-cfggen -m /etc/sonic/minigraph.xml -t /etc/swss/bgp/isolate.j2 >/usr/sbin/bgp-isolate
chown root:root /usr/sbin/bgp-isolate
chmod 0755 /usr/sbin/bgp-isolate

sonic-cfggen -m /etc/sonic/minigraph.xml -t /etc/swss/bgp/unisolate.j2 >/usr/sbin/bgp-unisolate
chown root:root /usr/sbin/bgp-unisolate
chmod 0755 /usr/sbin/bgp-unisolate

