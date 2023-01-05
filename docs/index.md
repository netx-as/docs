# Introduction

NETX Smart Router series were jointly developed with Brno University of Technology to provide high-performance and open-source
routing platform. NETX routers offer industry-standard routing and management protocols and support configuration through a command-line
interface (CLI) or via API.

NETX routers use `netc`, a custom and higly flexible command line tool that allows to configure a Linux based system in the same way as
network devices. Philosophy of `netc` operation is based on Cisco/Juniper or Mikrotik configuration styles.

The following NETX documentation topics are available:

* [Default configuration](default-config.md): Find out default NETX settings, such as login credentials, managament interface settings or serial console settings.
* [CLI](cli/netc-cli.md): Familiarize with basic concept of `netc` CLI. Describes differences between unix and netc shell, context switching, etc.
* [Configuration files](system/system-config.md): NETX routers use `startup` and `running` config files concept. This section describes basic commands that can be used for working with configs.
* [Basic configuration](system/basics.md): Describes basic system settings - changing hostname, time and NTP settings, user management and password recovery.
* [L2 configuration](l2/l2-config.md): Layer 2 config options - interface types, VLAN, link aggregations, interface statistics, etc.
* [L3 configuration](l3/l3-basics.md): IP address configuration, listing ARP/ND caches, routing table or setting up static routes.
* [Routing](l3/l3-advanced.md): Advanced routing configuration, BGP, OSFP and RIP settings.
* [QoS](qos/traffic-shaping.md): Traffic shaping and integration with 3rd party management softwares and custom scripts.
* [VPN](vpn/wireguard.md): Describes WireGuard VPN integration in NetX routers.
* [Monitoring](monitoring/monitoring.md): SNMP and Zabbix integration allows to monitor various NetX properties, such as
Control Plane/Data Plane load, various QoS rules statistics and others.
* [High availability](ha/vrrp.md): Describes how to set Virtual Router Redundancy Protocol to achieve high availability for default gateway.
* [Troubleshooting tools](tools/tshoot.md): Describes basic troubleshooting tools - e.g., `ping`, `traceroute` or `tcpdump`.
* [NetFlow export](netflow/netflow.md): NetFlow export configuration and accounting.
* [Event manager](event/event.md): Event managers allows to define actions when certain events occurs.
* [API](api/api.md): REST API documentation and basic examples.
