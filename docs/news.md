# What's new

This page provides a summary of new features in each release of `netc` CLI. 

## Version 1.19.2

### New features and notable changes
* Allow to display content of a custom firewall script
* Export network card driver version via statsd
* traffic manager MUST be enabled using `enable` command in traffic-manager context
* Support for [Adminus CRM](https://www.adminus.cz/)
* Allow to set strings with whitespace characters (e.g. description, etc.) all strings are escaped with quotes
* Add support for multiple NetFlow collectors
* Display total traffic and CPU usage in `show system` command
* Allow to set qos-rules using netc CLI 

### Fixed issues
* fix various integration issues with mango CRM
* fix default flow-cache size
* fix `show ipv4` alignment

## Version 1.19.1

### New features and notable changes
* Add support for a per-client setting of a shaping algorithm
* Introduce a priority setting for a client. The meaning of priority is the percent of bandwidth that is guaranteed for the node. The rest of the bandwidth can be distributed amongst nodes with higher priority.

### Fixed issues
* Fix routing daemon statistics
* Adding an interface to a channel group keeps previous interface state
* Fix displaying route metric in running-config
* Show SQL query for traffic manager properly

## Version 1.19.0

### New features and notable changes
* Introduce a burst shaping - a client download/upload speed is altered in predefined steps
* Add enterprise NetX SNMP OID for precise monitoring CPU stats
* Allow force NTP sync
* LLDP daemon integration in netc
* Support for setting a custom route metric
* Allow reporting stats per client to [ISPadmin](https://ispadmin.eu) version 5

### Fixed issues
* Various fixes for macvlan interface
* Fix arp-reply settings to handle properly interfaces named with dots
* Resolves DDoS protector blackhole stats

## Version 1.18.2

### New features and notable changes
* Preload additional system SNMP information - MIB `1.3.6.1.4.1.2021`

### Fixed issues
* Fixed a memory leak in dtd deamon 

## Version 1.18.1

### New features and notable changes
* Add support for gathering additional statistics for every user with a traffic shaping class.
* Update DDoS protector integration
* Update out-of-band management, add firewall support for out-of-band interface

### Fixed issues
* Fix losing IPv6 configuration after reboot

## Version 1.18.0

### New features and notable changes
* Add DDoS Protector BGP integration
* Add concurrent file editing using [tmux](https://github.com/tmux/tmux/wiki) multiplexer
* Rewrite internal variable storing to a new DataTree daemon
* Add integration with [Mango ISP](https://www.ogsoft.cz/produkty-a-sluzby/pro-isp/mango-isp)
* Increase IPv6 routing table size
* Increase size of the connection tracking table
* Support for a new version of IPMI OOB  

### Fixed issues
* Align `show interface` output properly
* Fix firewall to set protocol before a port number
* Fix syslog service restarts
* Fix displaying hardware queues for some network cards

## Version 1.17.7

### Fixed issues
* Fixed module naming for X1102 platform
* Fix traffic manager to work with duplicate address properly

## Version 1.17.6

### New features and notable changes
* SNMP daemon is disabled by default
* Custom NTP configuration changes are allowed and work with NTP servers set by netc
* Shaping and statistics integration between NetX and [ISPadmin](https://ispadmin.eu/)

### Fixed issues
* Fix an issue when a shutdown interface removed from a channel-group doesn't stay offline

## Version 1.17.5

### New features and notable changes
* Allow arp/nd filtering according to IP address and interface, allow removing cache entries
* Disable DNS resolving for firewall rules
* Support for firewall log limit
* Add support for remote logging using syslog
* Add support for QinQ interfaces

### Fixed issues
* Fix showing devel release channel in running/startup-config
* Fix showing ipv6 firewall rules
* Fix SNMP info after netc update

## Version 1.17.4

### New features and notable changes
* Netflow: add support for promisc mode, gather statistics information
* sync-manager: add shaping coefficient option to allow easy set percentage overhead for customer's shaping. E.g., if a customer is shaped to 10 Mbit, shaping coefficient 1.1 allows exceeding the threshold by 10% 

### Fixed issues
* none

## Version 1.17.3

* Internal build without any changes

## Version 1.17.2

### Fixed issues
* Fix displaying static ipv4 routes
* Fix showing multiple port numbers in firewall rules

## Version 1.17.1

### New features and notable changes
* Allows ipv4/ipv6 neighbor cache clearing - see [ARP/Neighbour tables](~/docs/l3/l3-basics.md#arpneighbour-tables) for details
* Support dport range for firewall

### Fixed issues
* Don't show exit command in wrong contexts
* Fix error if only one PSU is installed

## Version 1.17.0

### New features and notable changes
* Support for Policy-Based Routing
* Support for NetFlow export
* Change dhclient to dhcpcd
* Change edit config behavior for bird config
* Traffic shaping redesign, better support for hierarchical shaping
* Support for setting DHCP in service module (DHCP is now default) 

### Fixed issues
* Fixed atomic processing of dumpdb file
* Fixed several issues with traffic manager output
* Fixed issues with shaping statistics and output

### HW Platform
* Support for HW platforms X2340 and X1240

## Version 1.16.0

### New features and notable changes
* Support for GRE tunneling
* Support for ISPadmin synchronization
* Redesign CPU load monitoring
* Add support for IPv6 nameserver

### Fixed issues
* Fix showing VRRP info
* Fix showing db-host in traffic-manager 
* Fix switching between kernels 
* Fix several displaying issues in traffic-manager
* Fix zabbix-agent permission issues 

## Version 1.15.2

### Fixes
* Fix displaying routes in running-config

## Version 1.15.1

### Fixes
* Fix CPU load monitoring on different platforms
* Don't show default MTU value in running-config

## Version 1.15.0

### New features and notable changes
* Added support for running DHCPv4/DHCPv6 server
* IPv6 address EUI can be generated based on EUI64 algorithm
* Zabbix support, Zabbix server can read any value supported by datatree
* Allows setting MTU value on an interface
* Support for precise monitoring of CPUs load
* Show ipv4/ipv6 interface displays if an address is configured via DHCP
* Support for multicast routing and traffic statistics per multicast group
* Support for SNMP configuration
* `show release channel` command is added
* ARP reply is now sent for any local target IP address, configured on any interface. Previously, the reply behavior was more strict

### Fixed issues
* IPv6 static routes are handled properly
* Default refresh time in statsd
* Fix `show running-config` freeze

### HW platform
* Added support for DDoS protector 100GBE NIC

## Version 1.14.0

### New features and notable changes
* Switch to semantic versioning of `netc` package
* Allow a modularity in netc and statsd apps
* Allow executing commands from the global context in the local context as well
* Redesign VRRP daemon, additional information about VRRP status and topology is printed
* Add default webpage
* Redesign gathering statistics to `statsd` daemon
* `https://host/stats` URL for gathering statistics changed to `https://host/dt`
* Add support for devel channel - switching to devel channel allows installing git netc RPMs
 
### Fixed issues
* Disable auto-creation of a dummy interface
* Several fixes in ipset and firewall outputs

### HW platform

* Initial support for CESNET DDoS Protector
* Support for X1103 platform

## Version 1.13

### New features

* bird2 is used as a default routing daemon
* Support for token-based API access - see [Token authentication](~/tutorials/api/token.md) tutorial for details
* Support for new X1102 hardware
* Add a serial number to `show system` command
* Performance optimization after spectre/meltdown patches

### Fixed issues

* Fix handling routes learned from DHCP
* Better detection between bird/bird2 routing instances
* ARP protocol will always use the best local address
* ARP will reply only if the target IP address is the local address configured on the incoming interface
* Unify outputs of error/warning messages

## Version 1.12

### New features

* DHCP support: IPv4 address can be configured via DHCP using `ipv4 address DHCP` in interface context
* reboot: `reboot` command in the global context can be used to reboot netx
* IPMI support: various IPMI features can be set in system context
* SPF info: information about supported SPF transceivers are displayed in the interface detail section
* Mirror: it's possible to mirror and truncate traffic to another interface
* Firewall: support for negative options
* Firewall: support for state options
* Kernel: add support for kernel selection in system context

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
