# High availability

Virtual Router Redundancy Protocol (VRRP) defined in [RFC 5798](https://tools.ietf.org/html/rfc5798) is designed to address an issue when default gateway for end clients fails. 
Using VRRP protocol, it is possible to create a group consisting several NETX routers to form a virtual router. The VRRP group has one master and multiple backups, and provides 
a virtual IP address. The hosts on the subnet use the virtual IP address as their default network gateway to communicate with external networks.

VRRP avoids single points of failure. When the master in the VRRP group fails, another router in the VRRP group takes over. The switchover is complete without causing dynamic 
route recalculation, route re-discovery, gateway reconfiguration on the hosts, or traffic interruption.

## Basic settings

It is possible to configure VRRP group in the interface context using `vrrp` command. The following example crete a VRRP group with virtual IPv4 address 192.168.1.254.

```
netx# interface ve2
netx(if-ve2)# vrrp 1 ipv4 192.168.1.254
```

`show ipv4 vrrp` command can be used to display details about the VRRP state, last transition, priority, etc. The command displays all configured VRRP groups if it is entered in
global context. If the command is entered in context of an interface, it displays only VRRP groups configured on the interface.

```
netx# show ipv4 vrrp
INTERFACE    VRRP ID PRIO       VIRTUAL IP    STATE        MASTER IP  LAST TRANSITION
ve2                1  100    192.168.1.254   BACKUP    192.168.1.100  Sat Nov  3 11:20:20 2018
```

Detailed information about the VRRP group can be displayed in the interface context using `show vrrp detail` command.

```
netx# interface ve2
netx(if-ve2)# show vrrp detail
Interface: ve2, VRRP ID: 1
   Accept: enabled
   Advert interval: 1 sec
   Authentication type: none
   Gratuitous ARP delay: 5
   Gratuitous ARP lower priority delay: 5
   Gratuitous ARP lower priority repeat: 5
   Gratuitous ARP refresh: 0
   Gratuitous ARP refresh repeat: 1
   Gratuitous ARP repeat: 5
   IP: 192.168.1.254/32 dev ve2 scope global
   Last transition: 1541240420 (Sat Nov  3 11:20:20 2018)
   Listening device: ve2
   Master priority: 100
   Master router: 192.168.1.100
   Preempt: enabled
   Priority: 100
   Promote_secondaries: disabled
   Send advert after receive higher priority advert: false
   Send advert after receive lower priority advert: true
   State: BACKUP
   Using src_ip: 192.168.1.102
   VRRP Version: 2
   Virtual Router ID: 1
```

## Set a priority

The NETX router assigned the highest priority becomes the master router. By default, priority is set to 100. It is possible to change the priority value by using
`priority` command. The following example shows how to change priority value for VRRP Group ID 1.

```
netx# interface ve2

! display vrrp info and check the priority
netx(if-ve2)# show vrrp
INTERFACE    VRRP ID PRIO       VIRTUAL IP    STATE        MASTER IP  LAST TRANSITION
ve2                1  100    192.168.1.254   BACKUP    192.168.1.100  Sat Nov  3 11:20:20 2018

! change priority to 150 to became a master node
netx(if-ve2)# vrrp 1 priority 150
netx(if-ve2)# show vrrp
INTERFACE    VRRP ID PRIO       VIRTUAL IP    STATE        MASTER IP  LAST TRANSITION
ve2                1  150    192.168.1.254   MASTER            local  Sat Nov  3 17:29:30 2018
