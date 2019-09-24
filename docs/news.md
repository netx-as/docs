# What's new

This page provides a summary of new features in each release of `netc` CLI. 

## Version 1.17.0

### New features and notable changes
* support for Policy Based Routing
* support for NetFlow export
* change dhclient to dhcpcd
* change edit config behavior for bird config
* traffic shaping redesign, better support for hierarchical shaping
* support for setting dhcp in service module (dhcp is now default) 

### Fixed issues
* fixed atomic processing of dumpdb file
* fixed several issues with traffic manager output
* fixed issues with shaping statistics and output

### HW Platform
* Support for HW platforms X2340 and X1240

## Version 1.16.0

### New features and notable changes
* support for GRE tunneling
* support for ISPadmin synchronization
* redesign CPU load monitoring
* add support for IPv6 nameserver

### Fixed issues
* fix showing VRRP info
* fix showing db-host in traffic-manager 
* fix switching between kernels 
* fix several displaying issues in traffic-manager
* fix zabbix-agent permission issues 

## Version 1.15.2

### Fixes
* fix displaying routes in running config

## Version 1.15.1

### Fixes
* fix CPU load monitoring on different platforms
* don't show default MTU value in running config

## Version 1.15.0

### New features and notable changes
* added support for running DHCPv4/DHCPv6 server
* IPv6 address EUI can be generated based on EUI64 algorithm
* Zabbix support, zabbix server can read any value supported by datatree
* Allows setting MTU value on interface
* Support for precise monitoring of CPUs load
* show ipv4/ipv6 interface displays if address is configured via DHCP
* support for multicast routing and traffic statistics per multicast group
* support for SNMP configuration
* show release channel command is added
* ARP reply is now sent for any local target IP address, configured on any interface. Previously, the reply behavior was more strict

### Fixed issues
* IPv6 static routes are handled properly
* default refresh time in statsd
* fix show running config freeze

### HW platform
* Added support for DDoS protector 100GBE NIC

## Version 1.14.0

### New features and notable changes
* switch to semantic versioning of `netc` package
* allows modularity in netc and statsd apps
* allow execute commands from global context in local context as well
* redesign VRRP daemon, print additional information about VRRP status and topology
* add default webpage
* redesign gathering statistics to `statsd` daemon
* `https://host/stats` url for gathering statistics changed to `https://host/dt`
* add support for devel channel - switching to devel channel allows to install git netc rpms
 
### Fixed issues
* disable autocreation of dummy interface
* several fixes in ipset and firewall output

### HW platform

* initial support for CESNET DDoS Protector
* support for X1103 platform

## Version 1.13

### New features

* bird2 is use as a default routing daemon
* support for token based API access - see [Token authentication](~/tutorials/api/token.md) tutorial for details
* support for new X1102 hardware
* add serial number to `show system` command
* performance optimization after spectre/meltdown patches

### Fixed issues

* fix handling routes learned from DHCP
* better detection between bird/bird2 routing instances
* ARP protocol will always use the best local address
* ARP will reply only if the target IP address is local address configured on the incoming interface
* unify outpus of error/warning messages

## Version 1.12

### New features

* dhcp support: IPv4 address can be configured via DHCP using `ipv4 address dhcp` in interface context
* reboot: `reboot` command in the global context can be used to reboot netx
* IPMI support: various IPMI features can be set in system context
* SPF info: information about supported SPF transievers are displayed in the interface detail section
* mirror: it's possible to mirror and/or truncate traffic to another interace
* firewall: support for negative options
* firewall: support for state options
* kernel: add support for kernel selection in system context

### Fixed issues

* traffd: properly close filehandle
* cli: fix `no login shell bash` command
* cli : bond: fix miimon default
* cli : fix multiple execution of traffd
* cli: fix user deletion
* statsd: start statsd deamon automatically
* core : set irq affinity correctly using `set_irq_affinity` script
* statsd : fix interface stats
* api : fix API processing speed
