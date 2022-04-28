from .manager import Manager
from .template import TemplateFabric
from swsscommon import swsscommon
from .managers_rm import ROUTE_MAPS
import ipaddress
from .log import log_info, log_err


class AdvertiseRouteMgr(Manager):
    """This class Advertises routes when ADVERTISE_NETWORK_TABLE in STATE_DB is updated"""

    def __init__(self, common_objs, db, table):
        """
        Initialize the object
        :param common_objs: common object dictionary
        :param db: name of the db
        :param table: name of the table in the db
        """
        super(AdvertiseRouteMgr, self).__init__(
            common_objs,
            [],
            db,
            table,
        )

        self.directory.subscribe(
            [
                ("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME, "localhost/bgp_asn"),
            ],
            self.on_bgp_asn_change,
        )
        self.advertised_routes = dict()

    OP_DELETE = "DELETE"
    OP_ADD = "ADD"

    def set_handler(self, key, data):
        log_info("AdvertiseRouteMgr:: set handler")
        if not self._set_handler_validate(key, data):
            return True
        vrf, ip_prefix = self.split_key(key)
        self.add_route_advertisement(vrf, ip_prefix, data)

        return True

    def del_handler(self, key):
        log_info("AdvertiseRouteMgr:: del handler")
        if not self._del_handler_validate(key):
            return
        vrf, ip_prefix = self.split_key(key)
        self.remove_route_advertisement(vrf, ip_prefix)

    def _ip_addr_validate(self, key):
        if key:
            _, ip_prefix = self.split_key(key)
            ip_prefix = ip_prefix.split("/")
            if len(ip_prefix) != 2:
                log_err("BGPAdvertiseRouteMgr:: No valid ip prefix for advertised route %s" % key)
                return False
            try:
                ip = ipaddress.ip_address(ip_prefix[0])
                if ip.version == 4 and int(ip_prefix[1]) not in range(0, 33):
                    log_err(
                        "BGPAdvertiseRouteMgr:: ipv4 prefix %s is illegal for advertised route %s" % (ip_prefix[1], key)
                    )
                    return False
                if ip.version == 6 and int(ip_prefix[1]) not in range(0, 129):
                    log_err(
                        "BGPAdvertiseRouteMgr:: ipv6 prefix %s is illegal for advertised route %s" % (ip_prefix[1], key)
                    )
                    return False
            except ValueError:
                log_err("BGPAdvertiseRouteMgr:: No valid ip %s for advertised route %s" % (ip_prefix[0], key))
                return False
        else:
            return False
        return True

    def _set_handler_validate(self, key, data):
        if data:
            if "profile" in data and data["profile"] not in ROUTE_MAPS:
                log_err("BGPAdvertiseRouteMgr:: No valid profile for advertised route %s" % data)
                return False
            elif data != {"": ""}:
                log_err("BGPAdvertiseRouteMgr:: Invalid data for advertised route %s" % data)
                return False
        return self._ip_addr_validate(key)

    def _del_handler_validate(self, key):
        return self._ip_addr_validate(key)

    def add_route_advertisement(self, vrf, ip_prefix, data):
        if self.directory.path_exist("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME, "localhost/bgp_asn"):
            if not self.advertised_routes.get(vrf, dict()):
                self.bgp_network_import_check_commands(vrf, self.OP_ADD)
            self.advertise_route_commands(ip_prefix, vrf, self.OP_ADD, data)

        self.advertised_routes.setdefault(vrf, dict()).update({ip_prefix: data})

    def remove_route_advertisement(self, vrf, ip_prefix):
        if ip_prefix not in self.advertised_routes.get(vrf, dict()):
            log_info("BGPAdvertiseRouteMgr:: %s|%s does not exist" % (vrf, ip_prefix))
            return
        self.advertised_routes.get(vrf, dict()).pop(ip_prefix)
        if not self.advertised_routes.get(vrf, dict()):
            self.advertised_routes.pop(vrf, None)

        if self.directory.path_exist("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME, "localhost/bgp_asn"):
            if not self.advertised_routes.get(vrf, dict()):
                self.bgp_network_import_check_commands(vrf, self.OP_DELETE)
            self.advertise_route_commands(ip_prefix, vrf, self.OP_DELETE)

    def advertise_route_commands(self, ip_prefix, vrf, op, data=None):
        is_ipv6 = TemplateFabric.is_ipv6(ip_prefix)
        bgp_asn = self.directory.get_slot("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME)["localhost"][
            "bgp_asn"
        ]
        cmd_list = []
        if vrf == "default":
            cmd_list.append("router bgp %s" % bgp_asn)
        else:
            cmd_list.append("router bgp %s vrf %s" % (bgp_asn, vrf))

        cmd_list.append(" address-family %s unicast" % ("ipv6" if is_ipv6 else "ipv4"))

        if data and "profile" in data:
            cmd_list.append("  network %s route-map %s" % (ip_prefix, "%s_RM" % data["profile"]))
            log_info(
                "BGPAdvertiseRouteMgr:: Update bgp %s network %s with route-map %s"
                % (bgp_asn, vrf + "|" + ip_prefix, "%s_RM" % data["profile"])
            )
        else:
            cmd_list.append("  %snetwork %s" % ("no " if op == self.OP_DELETE else "", ip_prefix))
            log_info(
                "BGPAdvertiseRouteMgr:: %sbgp %s network %s"
                % ("Remove " if op == self.OP_DELETE else "Update ", bgp_asn, vrf + "|" + ip_prefix)
            )

        self.cfg_mgr.push_list(cmd_list)
        log_info("BGPAdvertiseRouteMgr::Done")

    def bgp_network_import_check_commands(self, vrf, op):
        bgp_asn = self.directory.get_slot("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME)["localhost"][
            "bgp_asn"
        ]
        cmd_list = []
        if vrf == "default":
            cmd_list.append("router bgp %s" % bgp_asn)
        else:
            cmd_list.append("router bgp %s vrf %s" % (bgp_asn, vrf))
        cmd_list.append(" %sbgp network import-check" % ("" if op == self.OP_DELETE else "no "))

        self.cfg_mgr.push_list(cmd_list)

    def on_bgp_asn_change(self):
        if self.directory.path_exist("CONFIG_DB", swsscommon.CFG_DEVICE_METADATA_TABLE_NAME, "localhost/bgp_asn"):
            for vrf, ip_prefixes in self.advertised_routes.items():
                self.bgp_network_import_check_commands(vrf, self.OP_ADD)
                for ip_prefix in ip_prefixes:
                    self.add_route_advertisement(vrf, ip_prefix, ip_prefixes[ip_prefix])

    @staticmethod
    def split_key(key):
        """
        Split key into vrf name and prefix.
        :param key: key to split
        :return: vrf name extracted from the key, ip prefix extracted from the key
        """
        if "|" not in key:
            return "default", key
        else:
            return tuple(key.split("|", 1))
