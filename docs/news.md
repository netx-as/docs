# What's new

This page provides a summary of new features in each release of `netc` CLI. 

#### Version 1.23.1

**New features and notable changes**

* PPPoE-server: better integration

**Fixed issues**

* lldp neighbor discovery fix
* x13 platform support fixes

#### Version 1.23.0

**New features and notable changes**

* x13 platform support
* clustering support
* DHCPv6 relay: support for creating IPv6 routes from IA_PD messages
* traffic-manager: use new llq qdisc

**Fixed issues**

* ddos-guard: multiple fixes and improvements
* sync-manager: improvements in stability and performance

#### Version 1.22.3

**Fixed issues**

* bond interface: fix setting mtu
* dhcp-server: fix nameserver issue
* static routing: fix disappearing routes
* traffic-manager: statistics processing fixes

#### Version 1.22.2

**New features and notable changes**

* Redesigned packet scheduler
* dhcp-relay support
* System update via proxy server support
* ddos-guard: internal redesign, lower resource requirements
* Bridge interface: bridge-pass-filtering option
* traffic-manager: statistics processing speedup
* Shaper interface: pcq support - creating classes based on various parameters

**Fixed issues**

* sync-manager: adminus IPv6 support
* ddos-guard: using default template

#### Version 1.22.1

**New features and notable changes**

* Shaper interface: qos-type support

**Fixed issues**

* PPPoE-server: show status properly
* Shaper interface: switching up/down the interface
* traffic-manager: fixes related to shaper interfaces
* firewall: fix showing tables


#### Version 1.22.0

**New features and notable changes**

* Event manager: binding actions to various events
* Blackhole interface support
* traffic-manager: ecn support for sfq
* Checking for default password change
* Shaper interface feature from experimnetal to stable
* PPPoE-server experimental support

**Fixed issues**

* ddos-guard: removing rules, refreshing counters
* ddos-guard: mailing formating fixes
* NIC queue statistics fix


#### Version 1.21.3

**New features and notable changes**

* traffic-manager: Allow to switch between HFSC and HTB shaping algorithms
* traffic-manager: Increase number of HTB hierarchical levels
* traffic-manager: Allow to set guaranteed speeds for HTB
* sync-manager: Allow to ignore invalid certificates
* sync-manager: Adminus: support for setting [MARK](~/docs/qos/traffic-shaping.md#mark) option
* Add [Prometheus](https://prometheus.io/) exporter for exposing user's QoS traffic statistics

**Fixed issues**

* Password recovery fix for platform X12
* Properly displays default QoS shaping algorithm

---

#### Version 1.21.2

**New features and notable changes**

* traffic-manager: allow to select default QoS shaping algorithm

**Fixed issues**

* sync-manager: correctly marking active/inactive users from Adminus

---

#### Version 1.21.1

**New features and notable changes**

* sync-manager: new universal NetX API for Adminus (Adminus NetX modul required)

---

#### Version 1.21.0

**New features and notable changes**
* Traffic-manager: performance improvements
* DSCP support in ipv4/ipv6 firewall
* Separate statistics for controlplane and dataplane
* Show configuration performance improvements
* IPv4/IPv6 arp cache settings
* Service tags and NetX mac addresses added
* Firewall apply with timeout
* Experimental shaper interface feature
* Introduce `show sync-manager rules` command to show synchronized rules

**Fixed issues**
* Improvements in IPv6 routing
* NIC driver channels fix
* Various DDoS Guard fixes and improvements
* Various sync-manager fixes and improvements
* Sync-manager adminus synchronization improvements
* Sync-manager mango synchronization improvements
* Proper interface shutdown fix
* Password recovery fix on X12 platform
* Various buffering fixes
* Service module password modification fix

---

#### Version 1.20.1

**New features and notable changes**
* Introduce `show router bgp neighbor` command to show summary about BGP neighbors
* Add bridge support
* Support for `show ipv4/ipv6 sessions` to show/remove conntrack sessions in netc
* DDoS Guard: Add templates support and mail notification to 

**Fixed issues**
* fix info about saved configuration filename

---

#### Version 1.20.0

**Fixed issues**
* Various DDoS Guard fixes and improvements
* traffic-manager: CLI allow upload/download values without a suffix
* traffic-manager: CLI allow an empty parent in a shape command

---

#### Version 1.19.11

**Fixed issues**
* Various DDoS Guard fixes and improvements

---

#### Version 1.19.10

**New features and notable changes**
* Initial [DDoS Guard](~/docs/ddos/ddos-guard.md) support  

---

#### Version 1.19.9

**Fixed issues**
* Fix quotation during copy startup running command

---

#### Version 1.19.8

**New features and notable changes**
* traffic-manager: allows to set a mark option for a QoS rule in netc
* traffic-manager: remove comment when printing a QoS rule

---

#### Version 1.19.7

**New features and notable changes**
* sync-manager: Add support for increasing debug level
* sync-manager: Allows ISPAdming burst and adaptive shaping synchronization

---

#### Version 1.19.6

**New features and notable changes**
* sync-manager: support for adaptive shaping

**Fixed issues**
* sync-manager: fix updating rules

---

#### Version 1.19.5

**New features and notable changes**
* statsd: multithreaded support
* traffic-manager: allows select queueing discipline in CLI
* traffic-manager: allows to set ECN and queue limit 
* various offload features are supported to set via netc
* LLDP info can be displayed, LLDP can be disabled globally

**Fixed issues**
* Don't show global help context if there is a local context
* statsd - fix computing stats if shaping hierarchy is employed

---

#### Version 1.19.4

**Fixed issues**
* sync-manager: fix selecting default internal database

---

#### Version 1.19.3

**New features and notable changes**
* If a kernel panic is detected, NetX router is automatically rebooted after 60s
* traffic-manager: add half-duplex shaping support
* traffic-manager: add support for burst traffic
* Add support for wireguard VPN

**Fixed issues**
* fix to show LLDP neighbors properly
* fix to properly show netflow export status
* fix Adminus sync if speed is missing
* bond: fix adding/removing interface in bond
* fixed paginated output to show all lines properly

---

#### Version 1.19.2

**New features and notable changes**
* Allow to display content of a custom firewall script
* Export network card driver version via statsd
* traffic manager MUST be enabled using `enable` command in traffic-manager context
* Support for [Adminus CRM](https://www.adminus.cz/)
* Allow to set strings with whitespace characters (e.g. description, etc.) all strings are escaped with quotes
* Add support for multiple NetFlow collectors
* Display total traffic and CPU usage in `show system` command
* Allow to set qos-rules using netc CLI 

**Fixed issues**
* fix various integration issues with mango CRM
* fix default flow-cache size
* fix `show ipv4` alignment

---

#### Version 1.19.1

**New features and notable changes**
* Add support for a per-client setting of a shaping algorithm
* Introduce a priority setting for a client. The meaning of priority is the percent of bandwidth that is guaranteed for the node. The rest of the bandwidth can be distributed amongst nodes with higher priority.

**Fixed issues**
* Fix routing daemon statistics
* Adding an interface to a channel group keeps previous interface state
* Fix displaying route metric in running-config
* Show SQL query for traffic manager properly

---

#### Version 1.19.0

**New features and notable changes**
* Introduce a burst shaping - a client download/upload speed is altered in predefined steps
* Add enterprise NetX SNMP OID for precise monitoring CPU stats
* Allow force NTP sync
* LLDP daemon integration in netc
* Support for setting a custom route metric
* Allow reporting stats per client to [ISPadmin](https://ispadmin.eu) version 5

**Fixed issues**
* Various fixes for macvlan interface
* Fix arp-reply settings to handle properly interfaces named with dots
* Resolves DDoS protector blackhole stats

---

## Older release information

The older release information can be found [here](~/docs/news-archive.md)
