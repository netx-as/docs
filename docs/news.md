# What's new

This page provides a summary of new features in each release of `netc` CLI. 

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
