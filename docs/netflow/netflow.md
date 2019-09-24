# NetFlow export

Since `netc` version `1.17.0`, NetX routers can be configured for NetFlow v5, v9 or IPFIX flow data export. The
following list highlights some features supported by the NetFlow export.

* Full IPv6 support: Using NetFlow v9 or IPFIX, it's possible to export information about IPv6 traffic.
* NAT translations events: If NAT is configured on NetX router, information about creation/deletion of the NAT translation 
  can be exported using NetFlow Event Logging (NEL) extension.  
* SNMP agent for remote management and monitoring 
* High performance and scalability: It's possible to handle 10Gbit traffic together with all other enabled NetX features,
  such as shaping, firewall, etc.

## Configuration

The following options can be configured:

* __active-timeout__: Flows active timeout in seconds. NetX router will export active flows from the cache to the
  collector after reaching `active-timeout`. Default value 30 seconds.
* __collector__: NetFlow collector IP address and port. If only IP address is given, default UDP port 2055 will be used. 
* __inactive-timeout__: Inactive timeout in seconds. If a flow does not see any packet within this timeout, the flow
  will be exported to the collector. Default value 15 seconds.
* __natevents__: Collect and send NAT translation events as NetFlow Event Logging (NEL) extension for NetFlow v9/IPFIX.
  Default value is disabled.
* __protocol__: NetFlow protocol version. Supported versions are 5, 9 and 10 (10 means IPFIX). For IPv6 accounting it's
  necessary to use NetFlow version 9 or IPFIX. Default value is NetFlow v9.
* __template-refresh__: Templates refresh interval (packets). Default value 20. Only for v9 and IPFIX.
* __template-timeout__: Templates resend interval (mins). Default value 1 min. Only for v9 and IPFIX. 

NetFlow export can be configured by switching to the `netflow` context using `netflow` command.

```
netx# netflow 
netx(netflow)
```

To enable NetFlow export, the following two steps are necessary.

1. Set a collector IP address. E.g.:

```
netx# netflow
netx(netflow)# collector 192.0.2.1
```
2. Add a firewall rule to enable NetFlow accounting. In the following example, all traffic going through NetX router
(FORWARD chain) is accounted.

```
netx(netflow)# exit

! change to the ipv4 firewall context
netx# ipv4 firewall table filter chain FORWARD
netx(fw4-filter-FORWARD)# action NETFLOW
```

> [!NOTE]
> __License key__: NetX allows by default 100 000 active flows in the flow-cache. License key is required for higher number of flows. 

## Display configuration

It's possible to use `show netflow` command to display information about NetFlow export.

```
Status:                  disabled
Protocol version:        9
NetFlow collector:       192.0.2.1:2055
License key:             XXXXXXXXXXXXXX
Active timeout:          30
Inactive timeout:        15
Export NAT events:       disabled
Max. flows               2000000
Template timeout rate:   Every 1 min
Template refresh rate:   Every 20 packets
```
