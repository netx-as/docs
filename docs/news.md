# What's new

This page provides a summary of new features in each release of `netc` CLI. 

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
