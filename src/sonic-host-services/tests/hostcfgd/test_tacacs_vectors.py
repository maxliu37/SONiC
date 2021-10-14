from unittest.mock import call

"""
    hostcfgd test tacacs vector
"""
HOSTCFGD_TEST_TACACS_VECTOR = [
    [
        "TACACS",
        {
            "config_db_local": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "hostname": "radius",
                    }
                },
                "FEATURE": {
                    "dhcp_relay": {
                        "auto_restart": "enabled",
                        "has_global_scope": "True",
                        "has_per_asic_scope": "False",
                        "has_timer": "False",
                        "high_mem_alert": "disabled",
                        "set_owner": "kube",
                        "state": "enabled"
                    },
                },
                "KDUMP": {
                    "config": {
                        "enabled": "false",
                        "num_dumps": "3",
                        "memory": "0M-2G:256M,2G-4G:320M,4G-8G:384M,8G-:448M"
                        }
                },
                "AAA": {
                    "authentication": {
                        "login": "local" 
                        "debug": "True",
                    },
                    "authorization": {
                        "login": "local" 
                    },
                    "accounting": {
                        "login": "local" 
                    }
                },
                "TACPLUS": {
                    "global": {
                        "auth_type": "pap",
                        "timeout": "5"
                    }
                },
                "TACPLUS_SERVER": {
                    "192.168.1.1": {
                        "timeout": "10"
                    }
                },
            },
            "config_db_tacacs": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "hostname": "radius",
                    }
                },
                "FEATURE": {
                    "dhcp_relay": {
                        "auto_restart": "enabled",
                        "has_global_scope": "True",
                        "has_per_asic_scope": "False",
                        "has_timer": "False",
                        "high_mem_alert": "disabled",
                        "set_owner": "kube",
                        "state": "enabled"
                    },
                },
                "KDUMP": {
                    "config": {
                        "enabled": "false",
                        "num_dumps": "3",
                        "memory": "0M-2G:256M,2G-4G:320M,4G-8G:384M,8G-:448M"
                        }
                },
                "AAA": {
                    "authentication": {
                        "login": "local" 
                        "debug": "True",
                    },
                    "authorization": {
                        "login": "tacacs+" 
                    },
                    "accounting": {
                        "login": "tacacs+" 
                    }
                },
                "TACPLUS": {
                    "global": {
                        "auth_type": "pap",
                        "timeout": "5"
                    }
                },
                "TACPLUS_SERVER": {
                    "192.168.1.1": {
                        "timeout": "10"
                    }
                },
            },
            "config_db_local_and_tacacs": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "hostname": "radius",
                    }
                },
                "FEATURE": {
                    "dhcp_relay": {
                        "auto_restart": "enabled",
                        "has_global_scope": "True",
                        "has_per_asic_scope": "False",
                        "has_timer": "False",
                        "high_mem_alert": "disabled",
                        "set_owner": "kube",
                        "state": "enabled"
                    },
                },
                "KDUMP": {
                    "config": {
                        "enabled": "false",
                        "num_dumps": "3",
                        "memory": "0M-2G:256M,2G-4G:320M,4G-8G:384M,8G-:448M"
                        }
                },
                "AAA": {
                    "authentication": {
                        "login": "local" 
                        "debug": "True",
                    },
                    "authorization": {
                        "login": "tacacs+ local" 
                    },
                    "accounting": {
                        "login": "tacacs+ local" 
                    }
                },
                "TACPLUS": {
                    "global": {
                        "auth_type": "pap",
                        "timeout": "5"
                    }
                },
                "TACPLUS_SERVER": {
                    "192.168.1.1": {
                        "timeout": "10"
                    }
                },
            },
            "config_db_disable_accounting": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "hostname": "radius",
                    }
                },
                "FEATURE": {
                    "dhcp_relay": {
                        "auto_restart": "enabled",
                        "has_global_scope": "True",
                        "has_per_asic_scope": "False",
                        "has_timer": "False",
                        "high_mem_alert": "disabled",
                        "set_owner": "kube",
                        "state": "enabled"
                    },
                },
                "KDUMP": {
                    "config": {
                        "enabled": "false",
                        "num_dumps": "3",
                        "memory": "0M-2G:256M,2G-4G:320M,4G-8G:384M,8G-:448M"
                        }
                },
                "AAA": {
                    "authentication": {
                        "login": "local" 
                        "debug": "True",
                    },
                    "authorization": {
                        "login": "local" 
                    },
                    "accounting": {
                        "login": "disable" 
                    }
                },
                "TACPLUS": {
                    "global": {
                        "auth_type": "pap",
                        "timeout": "5"
                    }
                },
                "TACPLUS_SERVER": {
                    "192.168.1.1": {
                        "timeout": "10"
                    }
                }
            }
        }
    ]
]
