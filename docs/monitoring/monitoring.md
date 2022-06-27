# NetX hardware monitoring

NetX can be monitored using standard network protocols, such as SNMP or with other advanced
network monitoring systems, such as [Zabbix](https://www.zabbix.com/).

## SNMP

By default, the SNMP configuration is disabled on the NetX router and it's necessary to
configure a community string. Contact or a location can be configured as well, directly
from a netc CLI. 

### Commands

SNMP configuration can be configured in `system` context using `snmp-server`
command.

#### snmp-server community

Configure a SNMP server community and enable SNMP daemon.

##### Syntax

`snmp-server community <community-string>`

##### Example

```
snmp-server community netx-test
```

##### Default value

SNMP is disabled by default. No community string is configured.

---

#### snmp-server contact

Configure a contact information as reported by SNMP.

##### Syntax

`snmp-server contact <contact-info>`

##### Example

```
snmp-server contact noc@example.com
```

---

#### snmp-server location

Configure a location of the device as reported by SNMP.

##### Syntax

`snmp-server location <location-info>`

##### Example

```
snmp-server location "DC Brno"
```

---

### Configuration example

The following steps describe the basic settings:

1. Set a community string for SNMP.

```
netx# system snmp-server community netx-test

```

2. Optionally set a contact and location information

```
netx# system snmp-server location Brno
netx# system snmp-server contact noc@mydomain.com

```

3. It should be possible to check if everything is set-up correctly, e.g. using
`snmpwalk`. 

```
netx# shell
[root@netx ~]# snmpwalk -v2c -c netx-test 127.0.0.1 SNMPv2-MIB::sysDescr.0
SNMPv2-MIB::sysDescr.0 = STRING: NetX-cloud: 1.21.3.10.gf7e6f60, NetXOS release 7.8.2003 (Core) 5.4.186-1.7.el7.netx.x86_64
```

### NetX MIB

There are several standard MIB OIDs enabled by default, such as [system](https://oidref.com/1.3.6.1.2.1.1),
[hrSystemUptime](https://oidref.com/1.3.6.1.2.1.25.1.1), [ifMIB](https://oidref.com/1.3.6.1.2.1.31) and
[interfaces](https://oidref.com/1.3.6.1.2.1.2). 

Custom NetX properties, such as Control Plane and Data Plane utilization, more precise CPU core load and various traffic-manager
values can be queried using NetX MIB with OID `.1.3.6.1.4.1.55203`. The NetX MIB can be downloaded [here](mibs/NETX-MIB.txt) or
is available at standard location `/usr/share/snmp/mibs/`.

## Zabbix

Zabbix is an open-source software tool to monitor IT infrastructure such as networks, servers,
virtual machines, and cloud services. NetX supports monitoring and integration with Zabbix and it's possible
to configure an integration with Zabbix directly in netc CLI. By default, NetX
uses [Zabbix Active agent](https://blog.zabbix.com/zabbix-agent-active-vs-passive/9207/) with a custom template for
monitoring custom properties.

### Commands

Zabbix server can be configured in `system` context using `zabbix`
command.

#### zabbix hostname

Configure a unique, case sensitive hostname. Required for active checks and must match
hostname as configured on the Zabbix server.

##### Syntax

`zabbix hostname <hostname>`

##### Example

```
zabbix hostname rt.lab.netx.as
```

---

#### zabbix server

Configure a case sensitive hostname of Zabbix server or Zabbix proxy. It is possible to configure
several zabbix servers to export statistics to multiple servers or proxies.

##### Syntax

`zabbix server <domain-name|ip>`

##### Example

The following example exports data to both servers zabbix1 and zabbix2.
```
zabbix server zabbix1.netx.as
zabbix server zabbix2.netx.as
```

---

## Zabbix templates

The following Zabbix templates are available for NetX and allow to monitor different NetX properties.

* [NetX Base template](templates/zabbix-netx-base.xml): The basic NetX Zabbix template that monitors several HW stats, such as
Control Plane/Data Plane loads, network interfaces bps/pps statistics, etc. 
* [NetX Bird template](templates/zabbix-netx-bird.xml): The NetX Bird template automatically discovers BGP peers monitor their
status and number of exported/imported routes. If a BGP peer is down a trigger is reported.
* [NetX NetFlow template](templates/zabbix-netx-netflow.xml): Monitors NetFlow statits, such as number of flows in NetFlow cache,
total number of bytes, etc.
* [NetX QoS stats template](templates/zabbix-netx-qos-stats.xml): Autodiscovers all QoS shaping rules. **Does not** monitor bps/pps per
rule by default, as there could be large number of rules. Monitoring of each group can be handled by [zabbix-qos](templates/zabbix-qos)
script that use `zabbix-sender`.

> [!WARNING]
> There could be a large number of Zabbix items for QoS rules. Each QoS rule (a customer) creates three zabbix items by default.
> E.g., 5k customers creates 15k zabbix items are created. It's recommanded to use the zabbix-qos script that pushes the data using
> `zabbix-sender` as standard zabbix-agent, either passive or active, cannot handle this large amount of updates per second.

