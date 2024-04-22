# L2 configuration

This chapter discusses the various types of network interfaces on NETX router, how to configure interface-level settings, VLANs, Link
aggregation (port-channel in Cisco terminology), and other L2 features.

## Interface types

`netc` distinguishes several types of interfaces. Each interface is identified by a prefix name and a number based on the interface position in NETX chassis.
Numbers follow standard switch convention - numbers are increased from top to down, and from left to right. Expansion cards use card's slot number as a 
prefix for their interfaces (e.g., `tge11` for first interface in expansion slot 1). `netc` uses the following prefix names for different types of 
network interfaces:

| Prefix name | Description                      |
|-------------|----------------------------------|
| fe          | 100 Mbps Ethernet Interface      |
| ge          | 1 Gbps  Ethernet Interface       |
| tge         | 10 Gbps Ethernet Interface       |
| fge         | 40 Gbps Ethernet Interface       |
| hge         | 100 Gbps Ethernet Interface      |
| ve          | virtual interface in NetX Cloud  |
| bond        | Link aggregation interface       |
| bridge      | virtual interface for bridging multiple interfaces |
| vxlan       | vxlan interface                  |
| lo          | loopback interface               |
| shaper      | shaper interface                 |

The command `show interface` displays basic information and traffic statistics for all interfaces.

```
netx# show interface
INTERFACE       STATE          RX                    TX
                          b/s      p/s          b/s      p/s
lo1                       0.0      0.0          0.0      0.0
bond0          10G-FD     9.8M    15.1k         9.3M    14.9k
bond0.110      10G-FD   340.6k   622.6        296.0k   624.1  main-backbone
ge1              down     0.0      0.0          0.0      0.0
<snip>
```

Interface specific configuration can be displayed by extending the `show interface` command with an interface name. E.g.

```
netx# show interface ge1
Device:              ge1
HW Address:          ac:1f:6b:22:c1:69
Oper status:         up
IP Address:          100.90.110.6/24
IP Address:          fe80::ae1f:6bff:fe22:c169/64
MTU:                 1500
STATISTICS                    RX                         TX 
                        total     per/sec          total     per/sec
Bytes,bits/s          1206.3k      25.7k          152.0k       7.6k
packets                 19.0k      42.5           929.0        7.7 
multicast              341.0        0.6              --        0.0 
dropped                341.0        0.6             0.0        0.0 
errors                   0.0        0.0             0.0        0.0 
```

Detailed statistics can be shown by adding `detail` keyword -- `show interface ge1 detail`

```
show interface ge1 detail 
Device:              ge1
HW Address:          ac:1f:6b:22:c1:69
Driver, fw:          igb-5.4.0-k1.63, 0x800009fa, fw:1.63, 0x800009fa
Oper status:         up
IP Address:          100.90.110.6/24
IP Address:          fe80::ae1f:6bff:fe22:c169/64
MTU:                 1500
STATISTICS                    RX                         TX 
                        total     per/sec          total     per/sec
Bytes,bits/s             1.9M      16.1k          213.3k     824.2 
packets                 30.2k      32.7          1262.0        1.0 
multicast              529.0        0.5              --        0.0 
dropped                529.0        0.5             0.0        0.0 
errors                   0.0        0.0             0.0        0.0 
fifo_errors              0.0        0.0             0.0        0.0 
frame_errors             0.0        0.0              --        0.0 
length_errors            0.0        0.0              --        0.0 
over_errors              0.0        0.0              --        0.0 
crc_errors               0.0        0.0              --        0.0 
missed_errors            0.0        0.0              --        0.0 
aborted_errors            --        0.0             0.0        0.0 
carrier_errors            --        0.0             0.0        0.0 
heartbeat_errors          --        0.0             0.0        0.0 
window_errors             --        0.0             0.0        0.0 
```

Every interface can also have a short description that is shown by `show interface` or `monitor interface` commands. 

```
netx# interface ge1
netx(if-ge1)# description mgmt
netx(if-ge1)# show description
mgmt
```

> [!NOTE]
> If there is a standard `ifcfg` config file for an interface in `/etc/syscofig/network-scripts/`, `netc` will ignore the interface and will
> not display the interface in running config.

## VLAN

VLAN (IEEE 802.1Q) is configured as a sub-interface. VLAN subinterface is created by adding the VLAN number after
the name of the parent interface. The parent interface and VLAN number are separated using `.` symbol.
The following command creates VLAN 112 on interface bond0.

```
netx# interface bond0.112
Creating vlan interface bond0.112
netx(if-bond0.112)#
```

## Loopback

A loopback interface is a virtual interface. The physical layer state of a loopback interface is always up unless the loopback
interface is manually shut down. It is possible to create a loopback interface using `interface lo<number>` command. E.g.:

```
netx# interface lo1
Creating loopback interface lo1
netx(if-lo1)#
```

Loopback interface can be deleted using `no interface lo<number>` command. E.g.

```
netx# no interface lo1
Removing loopback interface lo1
netx#
```

> [!NOTE]
> Default Linux loopback interface `lo` is ignored by `netc` and not displayed in running config. However, it is possible to edit `lo`
> settings using `interface lo` command without a problem.

## Shaper

A shaper interface is a virtual interface used for traffic shaping in [traffic-manager](~/docs/qos/traffic-shaping.md#interface). The physical layer state of a shaper interface is always up unless the shaper interface is manually shut down. It is possible to create a shaper interface using `interface shaper<number>` command. E.g.:

```
netx# interface shaper1
Creating shaper interface shaper1
netx(if-shaper1)#
```

Shaper interface can be deleted using `no interface shaper<number>` command. E.g.

```
netx# no interface shaper1
Removing shaper interface shaper1
netx#
```

Shaper0 serves as a unique shaper interface that handles all the traffic passing through the device. No specific firewall rules are necessary.

Sending traffic to shaper interface is posible using a traffic-manager or a firewall rule. E.g.

```
netx# ipv4 firewall table raw chain POSTROUTING
netx(fw4-raw-POSTROUTING)# action SHAPER shaper-ifc shaper1
```

## Link Aggregation

Multiple physical links can be grouped together into a single logical "bonded" interface. This offers a ways to increase performance and to 
provide redundancy so that the bond link is still active even if one of the physical link fails. The behavior of the bonded interface 
depends upon the mode - it can provide different ways of load balancing or active/backup 
links -- see [Link aggregation mode](l2-config.md#link-aggregation-mode) for details.

Follow the steps to create a new bond interface:  

1. Create a name for the link aggregation interface. The interface name must be constructed with the `bond`
prefix followed by a number.

```
netx# interface bond1
Creating link aggeragtion interface bond1
netx(if-bond1)# 
netx(if-bond1)# exit
```

2. Configure a bond mode. The default mode is `balance-rr`. The mode is changed to 802.3ad (LACP) using `port-channel` command. 

```
netx# interface bond1
netx(if-bond1)# port-channel mode 802.3ad
```

> [!NOTE]
> Bond mode must be set before physical links are assigned to the bond. 

3. Assign physical interfaces to the bond interface. In the following example 
`tge1` and `tge2` interfaces are assigned to `bond1` interface. 

```
netx# interface tge1
netx(if-tge1)# channel-group bond1
netx(if-tge1)# exit
netx# interface tge2
netx(if-tge2)# channel-group bond1
netx(if-tge2)# exit
```

The status of the bond interface can be checked using `show interface` command. 

```
netx# show interface bond1 
Device:              bond1
HW Address:          0c:c4:7a:87:2d:53
Oper status:         up
Link status:         20Gb/s Full
IP Address:          fe80::ec4:7aff:fe87:2d53/64
MTU:                 1500
Bond mode:           802.3ad
Bond slaves:         tge1 tge2
Bond hash policy:    layer2
Bond up/down delay:  0/0 ms
Bond lacp rate:      slow
Bond monitor freq.   100 ms
STATISTICS                    RX                         TX 
                        total     per/sec          total     per/sec
Bytes,bits/s           379.5G     179.2k          376.9G     166.8k
packets                350.4M      83.4           318.9M      61.4 
multicast              371.0k       1.3              --        0.0 
dropped                  0.0        0.0             0.0        0.0 
errors                   0.0        0.0             0.0        0.0 
```

Several additional parameters can be specified for the bond interface. These parameters are entered in 
the `port-channel` submenu.

### Link aggregation mode

Bond driver can operate in the following modes. The mode must be set before any physical interfaces are
assigned to the bond. 

| Mode  |  Description |
|-------|--------------|
| 802.3ad |  IEEE 802.3ad Dynamic link aggregation. All slaves interfaces are active. Slave selection for outgoing traffic is done according to the transmit hash policy (see below) |
| active-backup | Only one slave in the bond is active. A different slave becomes active if, and only if, the active slave fails. |
| balance-rr | Transmit packets in round robin fashion from the first available slave through the last. |

### Load balancing policy

It is also possible to select a hash policy for interface selection when using 802.3ad mode.
  
| Hash-policy   |    Description |
|-------------- |   ------------------|
| layer2 (default) | Uses XOR of hardware MAC addresses and packet type ID field to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave interface. |
| layer2+3   	| Uses a combination of L2 and L3 protocol information to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave interface. It provides a more balanced distribution of traffic than layer2 alone. |
| layer3+4      | Uses upper layer protocol information, when available, to generate the hash. This allows for traffic to a particular network peer to span multiple slaves, although a single connection will stick the same slave |
| encap2+3      | Uses the same formula as layer2+3 but uses also inner headers if an encapsulation protocol is used. For example this will improve the performance for tunnel users because the packets will be distributed according to the encapsulated flows. |
| encap3+4      | Uses the same formula as layer3+4 but uses of inner headers if an encapsulation protocol is used. The packets will be distributed according to the encapsulated flows. |

### Monitoring slave interfaces

Other parameter, that can be set is `miimon`. It specifies the link monitoring frequency 
in milliseconds. This determines how often the link state of each slave is inspected for 
link failures. The default value is 100 ms. 

The following example shows setting of a hash-policy and changing the monitoring frequency value.

```
netx# interface bond1
netx(if-bond1)# port-channel hash-policy layer2+3
netx(if-bond1)# port-channel miimon 200
netx(if-bond1)# exit
netx# show interface bond1
Device:              bond1
HW Address:          0c:c4:7a:87:2d:53
Oper status:         up
Link status:         20Gb/s Full
IP Address:          fe80::ec4:7aff:fe87:2d53/64
MTU:                 1500
Bond mode:           802.3ad
Bond slaves:         tge3 tge4
Bond hash policy:    layer2+3
Bond up/down delay:  0/0 ms
Bond lacp rate:      slow
Bond monitor freq.   200 ms
STATISTICS                    RX                         TX 
                        total     per/sec          total     per/sec
Bytes,bits/s           379.5G     155.3k          376.9G     142.8k
packets                350.4M      79.8           318.9M      55.0 
multicast              371.3k       1.0              --        0.0 
dropped                  0.0        0.0             0.0        0.0 
errors                   0.0        0.0             0.0        0.0 
```
