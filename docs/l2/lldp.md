# LLDP

Link Layer Discovery Protocol (LLDP) is a vendor-neutral link layer protocol used by network devices for advertising their identity, capabilities, and neighbors on an IEEE 802 local area network. NetX uses the standard `lldpd` daemon to provide this functionality.

## Configuration

LLDP is enabled by default on all interfaces. It can be disabled globally using the following command:

```
netx# lldp disable
```

To re-enable it, use the `no` form of the command:

```
netx# no lldp disable
```

## Monitoring

To view the status of LLDP and local chassis information, use the `show lldp` command. This command displays the status of the LLDP daemon and information about the local system that is being advertised to neighbors.

```
netx# show lldp
LLDP status     : enabled
Capability      : Router
ID              : 00:50:56:85:c1:92
Tx delay (s)    : 30
Description     : NetXOS 7 (Core) Linux 6.12.5-1.11.el7.netx.x86_64
Name            : Router-Edge-02
ManagementIP    : 192.168.1.10,fd00::1
```

### Viewing Neighbors

To view a summary of discovered LLDP neighbors, use the `show lldp neighbors` command. This provides a quick overview of connected devices.

```
netx# show lldp neighbors
INTERFACE       REMOTE DEVICE                      REMOTE PORT
tge1            Switch-Core-01                     GigabitEthernet1/0/1
tge2            Router-Edge-02                     tge1
```

For detailed information about neighbors, including capabilities, VLANs, and management addresses, use the `details` keyword:

```
netx# show lldp neighbors details
-------------------------------------------------------------------------------
Interface:    tge1, via: LLDP, RID: 3, Time: 12 days, 22:40:11
  Chassis:
    ChassisID:    mac 00:50:56:85:95:ef
    SysName:      Router-Edge-02
    SysDescr:     NetXOS 7 (Core) Linux 6.12.5-1.11.el7.netx.x86_64
    MgmtIP:       192.168.1.1
    MgmtIP:       fe80::250:56ff:fe85:95ef
    Capability:   Bridge, off
    Capability:   Router, on
    Capability:   Wlan, off
    Capability:   Station, off
  Port:
    PortID:       ifname tge1
    PortDescr:    tge1
    TTL:          120
    PMD autoneg:  supported: no, enabled: no
      MAU oper type: 10GigBaseCX4 - X copper over 8 pair 100-Ohm balanced cable
-------------------------------------------------------------------------------
```
