# L3 configuration #
This section describes configuration of the network layer. NETX supports IPv4 and IPv6 protocols with the same feature parity.

## IPv4 and IPv6 addresses
The configuration of IPv4 or IPv6 address is done in the interface context. Several IPv4 or IPv6 addresses can be configured
simultaneously on an interface.

```
netx# interface tge1
netx(if-tge1)# ipv4 address 192.0.2.1/24
netx(if-tge1)# ipv6 address 2001:db8:aaaa::1/64
```

It is possible to list IPv4 and IPv6 addresses using `show ipv4 interface` or `show ipv6 interface` command. 

```
netx# show ipv4 interface
bond0.111      up 100.90.111.3/24      
bond0.112      up 100.90.112.3/24

netx# show ipv6 interface
bond0.111      up 2001:db8:111::3/64  
bond0.112      up 2001:db8:112::3/64
```

Link-local addresses can be listed by using `link-local` keyword.

```
netx# show ipv6 interface link-local
bond0            up fe80::3efd:feff:fea2:32d0/64 
bond0.111        up 2001:db8:111::3/64  
                    fe80::8cee:6aff:fe64:bef7/64
bond0.112        up 2001:db8:112::3/64
                    fe80::8cee:6aff:fe64:bef7/64
```

## ARP/Neighbour tables

Bindings between protocol addresses and link layer addresses can be displayed using
`show ipv4 arp` or `show ipv6 neighbours`. These commands show hosts (neighbours) sharing 
the same link.

```
netx# show ipv4 arp
100.90.110.2 dev bond0.110 lladdr 00:50:56:b5:7c:7f REACHABLE
100.90.110.3 dev bond0.110 lladdr bc:ea:fa:6d:e3:1d STALE
100.90.110.8 dev bond0.110 lladdr 0c:c4:7a:0b:39:fa STALE

netx# show ipv6 neighbours
fe80::aa0c:dff:fe54:3eff dev bond0.1700 lladdr a8:0c:0d:54:3e:ff router STALE
fe80::5a8d:9ff:febf:5e80 dev bond0.1700 lladdr 58:8d:09:bf:5e:80 router STALE
2001:db8:87::1 dev bond0.1700 lladdr 00:15:c5:e6:e5:4b REACHABLE
2001:db8:87::23 dev bond0.1700 lladdr 80:ac:ac:3b:07:c8 router STALE
```

The neighbour entry can be in different states based on Neighbour Unreachability Detection algorithm. The state can take one of the following values:

* __PERNAMENT__ : the neighbour entry is valid forever and can be only be removed administratively.
* __NOARP__ : the neighbour entry is valid. No attempts to validate this entry will be made but it can be removed when its lifetime expires.
* __REACHABLE__ : the neighbour entry is valid until the reachability timeout expires.
* __STALE__ : the neighbor is no longer known to be reachable but until traffic is sent to the neighbor, no attempt is made to verify its reachability
* __NONE__ : this is a pseudo state used when initially creating a neighbour entry or after trying to remove it before it becomes free to do so.
* __INCOMPLETE__ the neighbour entry has not (yet) been validated/resolved.
* __DELAY__ : neighbor entry validation is currently delayed.
* __PROBE__ : the neighbor is no longer known to be reachable, probes are being sent to verify reachability.
* __FAILED__ : max number of probes exceeded without success, neighbor validation has ultimately failed.

## Routing table
Routes in NETX's forwarding table can be can be displayed by using `show ipv4 route` or `show ipv6 route` commands. If the NETX router has
significant number of routes, the command's output is paginated as in the following example.

```
! List IPv4 routes
netx# show ipv4 route
default via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 
1.0.4.0/24 via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 
1.0.4.0/22 via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 
1.0.5.0/24 via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 

<snip>

1.0.212.0/23 via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 
1.0.214.0/24 via 185.1.25.3 dev bond0.1700 proto bird src 185.135.134.1 
------ Q: quit   A: print all   <space> : continue -------


! List IPv6 routes
netx# show ipv6 route
2001::/32 via 2001:7f8:87::3 dev bond0.1700 proto bird src 2a07:6881:ffff:9::1 metric 1024 
2001:4:112::/48 via 2001:7f8:87::3 dev bond0.1700 proto bird src 2a07:6881:ffff:9::1 metric 1024 

<snip>

2001:2b8:50::/48 via 2001:7f8:87::3 dev bond0.1700 proto bird src 2a07:6881:ffff:9::1 metric 1024 
2001:2b8:51::/48 via 2001:7f8:87::3 dev bond0.1700 proto bird src 2a07:6881:ffff:9::1 metric 1024 
2001:2b8:52::/48 via 2001:7f8:87::3 dev bond0.1700 proto bird src 2a07:6881:ffff:9::1 metric 1024 
------ Q: quit   A: print all   <space> : continue -------
```

The routes can be learned from several different resources. If the route is set statically by a network administrator, it is
shown as a kernel route. If the route is learned by a routing daemon (e.g. OSPF, BGP or RIP), it is shown as a route learned
from `bird` protocol (the routing daemon used by NETX routers). 

### Static routes

IPv4 or IPv6 routes can be configured either in `netc` or via `bird` -- see [Advanced routing](l3-advanced.md) guide for details. To set up
a static route directly in `netc` use `ipv4/ipv6 route <prefix/len> <netxhop-ip>` syntax. The following example sets `192.0.2.0/24 via 198.51.100.1`.

```
netx# ipv4 route 192.0.2.0/24 198.51.100.1
! the same applies to IPv6
netx# ipv6 route 2001:db8:aaaa::/64 2001:db8:bbbb::1

! it's possible to show route via show ipv4 route or show ipv6 route commands
netx# show ipv4 route 192.0.2.0
default via 185.1.25.4 dev bond0.1700 proto bird src 185.217.234.1 metric 32 
192.0.2.0/24 via 100.90.110.1 dev bond0.192 

! show ipv6 route
netx# show ipv6 route 2001:db8:aaaa::/64
2001:db8:aaaa::/64 via 2001:db8:bbbb::1 dev ve4 metric 1024 
default via 2001:718:0:e710::2 dev bond0.1700 proto bird src 2a07:6881:0:ffff::2 metric 32 
``` 
