# What's new

This page provides a summary of new features in each release of `netc` CLI. 

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
