# Advanced Routing 

For more complex routing scenarios the NetX platform uses [bird](https://bird.network.cz/) routing daemon developed by CZ.NIC labs. The bird routing 
daemon is integrated to the `netc` interface. The bird integration in `netc` is divided into two parts:

* __bird config file:__ The bird config is created in a text editor and not part of the `netc` CLI. However, it's easy to switch between CLI and editing of
the config. The reason for that is that bird provides an amazing configuration language which is very clear and well arranged in the form of an edited file. 
* __control and diagnostics:__ Commands for showing protocols status, etc. are available via netc interface 

All bird related commands are available in `router bird` context. To enable bird routing daemon, use the following steps: 

1. Switch to `router bird` context 

```
netx# router bird
netx(router-bird)#
```

2. Define a configuration file. It's recommended to use bird.conf as the main config file if there is no reason to use a different one. If the file 
doesn’t exist `netc` will create a default minimal configuration which can be used as a template to build an own configuration. 

```
netx(router-bird)# config-file bird.conf 
ERROR: Building initial config file /etc/netc/bird/bird.conf
Starting bird
```

3. Use `edit` command to open an editor with the config file

```
netx(router-bird)# edit 

or

netx(router-bird)# config-file bird.conf edit 
```

4. Edit bird configuration. Please consult [bird documentation](https://bird.network.cz/?get_doc&f=bird.html&v=16) for the configuration syntax.

5. The edited configuration is not applied immediately, but `apply` command must be used. The command will check the config file syntax and, if everything
is correct, it will apply the config.

```
netx(router-bird)# apply 
```

> [!TIP]
> In some cases, it is useful to define a timeout before changes become permanent. If a timeout is defined, any changes will revert to the previous
> values if `confirm` command is not entered. This approach is useful to a prevent lockout, e.g., if a new filter for a BGP neighbor is set up. The 
> following example sets the timeout to 60s. During the timeout, `confirm` command must be entered, or the configuration is rolled back.
> 
> ```
> netx(router-bird)# apply timeout 60
> Configuration OK
> Undo scheduled in 60 s
> Reconfigured
>
> netx(router-bird)# confirm 
> Reconfiguration confirmed
> ```

## Bird version 1/2

NetX platform supports both Bird 1.x and Bird 2.x versions of routing daemons. The differences between those versions are outlined in the following table:

| Feature | Bird 1.x | Bird 2.x |
| ---     | ---      | ---      |
| Code stability | Stable | Stable / Experimental |
| Config file syntax stability | Stable | Incompatible changes can appear in future versions |
| Deployment | Critical Environments (IXPs, Core routers) | Standard Environment |
| IPv6 support | 2 separate routing process | Single routing process |
| MPLS | no | yes |
| FlowSpec | no | yes |
| RPKI | no | yes |
| NetX default | no | yes |
 
Bird 2 is the default version on NetX platform, and it's recommended to use. If you need to switch to Bird 1.x, please contact NetX Support 
(support@netx.as) for additional information.

## BGP routing example

In the following example, a simple configuration that connects NetX router to two BGP upstream peers is shown. One peer is a transit provider; the second 
peer is an exchange point. In the example, only the default route from the upstream peer is accepted. All available routes on route servers are accepted 
from IXP peer. Single IPv4 and IPv6 prefixes are announced to both upstream and IXP.

* At the first step, we set up a basic config with the necessary options to run bird.

```
log "/var/log/bird.log" all;
log syslog { info, remote, warning, error, auth, fatal, bug };

protocol device DEVICE { }

protocol direct DIRECT { ipv4; ipv6; }

protocol kernel KERNEL4 {
    ipv4 { export all; import none; };
}

protocol kernel KERNEL6 {
    ipv6 { export all; import none; };
}
```

We defined logging options and four essential protocols that every instance of bird needs to have. DEVICE and DIRECT protocols provide access to 
locally configured interfaces for both IPv4 and IPv6 protocols. KERNEL4 and KERNEL6 protocols define interfaces between internal bird routing 
structures and kernel’s IPv4 and IPv6 FIBs. We usually export all routes from internal bird routing table to kernel’s table. The kernel protocols 
must be defined separately for IPv4 and IPv6.

* When NetX is acting as a border BGP router, we will typically need to create a single static blackholed route that will be later propagated via 
BGP to our peers.  

```
protocol static STATIC4 {
    ipv4 { preference 110; };
    route 185.217.234.0/23 blackhole;
}

protocol static STATIC6 {
    ipv6 { preference 110; };
    route 2a07:6881::/32 blackhole;
}
```

* It's recommended to create templates to make the configuration clearer. A template doesn't represent any protocol, but it can be used later in protocol 
definition. The template can contain definitions for both IPv4 and IPv6 protocols (channels). 

```
template bgp T_UPSTREAM {
    local as myas;

    ipv4 {
        import filter {
            if ( net ~ [ 0.0.0.0/0 ] ) then accept;
            reject;
        };
        export filter {
            if ( net ~ [ 185.217.234.0/23 ] ) then accept;
            reject;
        };
    };

    ipv6 {
        import filter {
            if ( net ~ [ 0::/0 ] ) then accept;
            reject;
        };
        export filter {
            if ( net ~ [ 2a07:6881::/32 ] ) then accept;
            reject;
        };
    };

}
```

We defined input and output filters in the template. Input filters are simple - only default route from the upstream provider is accepted. This default 
route will be installed in FIB after the BGP session is established. The output filter defines which routes will be sent to an upstream provider. 
We set up the export filter to announce only routes that are allowed to announce to global BGP routing table from our ASN. In the example, we announce 
one IPv4 /23 and one /32 IPv6 route that we created in the previous step via static protocols.

* After setting up protocols and a template, we can establish BGP sessions towards upstream routers and route servers in an exchange point. The 
session UPS41 and UPS42 are IPv4 sessions to the upstream provider. Similar sessions are established for IPv6. 

```
protocol bgp UPS41  from T_UPSTREAM  { neighbor 147.229.252.114 as 197451; }
protocol bgp UPS42  from T_UPSTREAM  { neighbor 147.229.253.233 as 197451; }

protocol bgp UPS61  from T_UPSTREAM  { neighbor 2001:67c:1220:fa48::3 as 197451; }
protocol bgp UPS62  from T_UPSTREAM  { neighbor 2001:67c:1220:fa48::3 as 197451; }
```

* Another BGP sessions are established towards Route servers in an Exchange Point.  Only routes from route servers are accepted. This is done by 
changing default import filter from template by adding `ipv4 { import all; }`  or `ipv6 { import all; }` to the protocol definition.

```
protocol bgp IXP_RS41 from T_UPSTREAM { neighbor 185.1.25.1 as 60143; ipv4 { import all; } }
protocol bgp IXP_RS42 from T_UPSTREAM { neighbor 185.1.25.1 as 60143; ipv4 { import all; } }

protocol bgp IXP_RS61 from T_UPSTREAM { neighbor 2001:7f8:87::1 as 60143; ipv6 { import all; } }
protocol bgp IXP_RS62 from T_UPSTREAM { neighbor 2001:7f8:87::2 as 60143; ipv6 { import all; } }
```

## Display config, protocol status

It's possible to check status of bird by issuing `show protocols` in `router bird` context. E.g.:

```
netx(router-bird)# show protocols 
Name       Proto      Table      State  Since         Info
device1    Device     ---        up     2018-06-20    
DIRECT     Direct     ---        up     2018-06-20    
KERNEL4    Kernel     master4    up     2018-06-20    
KERNEL6    Kernel     master6    up     2018-06-20    
STATIC4    Static     master4    up     2018-06-20    
STATIC6    Static     master6    up     2018-06-20    
UPS41      BGP        ---        up     2018-06-20    Established   
UPS42      BGP        ---        up     2018-06-20    Established   
UPS61      BGP        ---        up     2018-06-20    Established   
UPS62      BGP        ---        up     2018-06-20    Established   
IXP_RS41   BGP        ---        up     2018-06-20    Established   
IXP_RS42   BGP        ---        up     2018-06-20    Established   
IXP_RS61   BGP        ---        up     2018-06-20    Established   
IXP_RS62   BGP        ---        up     2018-06-20    Established   
```

More detailed information related to each protocol can be obtained by `show protocols` command extended with bird protocol name.

```
netx(router-bird)# show protocols IXP_RS41
Name       Proto      Table      State  Since         Info
IXP_RS41   BGP        ---        up     2018-06-20    Established   
  BGP state:          Established
    Neighbor address: 185.1.25.1
    Neighbor AS:      60143
    Neighbor ID:      185.1.25.1
    Local capabilities
      Multiprotocol
        AF announced: ipv4 ipv6
      Route refresh
      Graceful restart
      4-octet AS numbers
      Enhanced refresh
    Neighbor capabilities
      Multiprotocol
        AF announced: ipv4
      Route refresh
      Graceful restart
      4-octet AS numbers
    Session:          external AS4
    Source address:   185.1.25.30
    Hold timer:       184.767/240
    Keepalive timer:  29.445/80
  Channel ipv4
    State:          UP
    Table:          master4
    Preference:     100
    Input filter:   (unnamed)
    Output filter:  (unnamed)
------ Q: quit   A: print all   <space> : continue -------
```

