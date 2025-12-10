# Routing 

> [!TIP]
> Check also the folowing tutorials:
> * [BGP: Set up peering between an exchange point and upstream provider](~/tutorials/bgp/basic-bgp.md)

For more complex routing scenarios the NetX platform uses [BIRD](https://bird.network.cz/) routing daemon developed by [CZ.NIC](https://www.nic.cz/). 
The BIRD routing daemon is integrated to the `netc` interface. The BIRD integration in `netc` is divided into two parts:

* __bird config file:__ The BIRD config file is created in a text editor, thus, routing commands are not integrated directly in `netc` CLI. The reason why 
NetX use BIRD config file is that BIRD provides a very clear configuration language designed for writing complex filters and routing policies. 
It is, however, very easy to switch between `netc` CLI and BIRD config.
* __control and diagnostics:__ Commands for showing protocols status, BGP/OSPF neighbors, and all other detailed information are available by switching to
internal BIRD CLI from `netc` interface 

All BIRD related commands are available in `router bird` context. To enable BIRD routing daemon, use the following steps: 

1. Switch to `router bird` context 

```
netx# router bird
netx(router-bird)#
```

2. Define a configuration file. It's recommended to use bird.conf as the main config file if there is no reason to use a different one. If the file 
doesn’t exist `netc` will create a default minimal configuration which can be used as a template to build an own configuration. 

```
netx(router-bird)# config-file bird.conf 
ERROR: No config file found. Building an initial config file in /etc/netc/bird/bird.conf
Starting bird
```

3. Use `edit` command to open an editor with the config file

```
netx(router-bird)# edit 

or

netx(router-bird)# config-file bird.conf edit 
```

4. Edit BIRD configuration. Please consult [BIRD documentation](https://bird.network.cz/?get_doc&f=bird.html&v=20) for the configuration syntax.

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

### Additional Router Commands

Besides the basic configuration workflow, the `router` context provides several other useful commands:

*   **check-config**: Validates the syntax of the current configuration file without applying it.
    ```
    netx(router-bird)# check-config
    ```

*   **protocols**: Displays the status of configured routing protocols directly within `netc`.
    ```
    netx(router-bird)# protocols
    name     proto    table    state  since       info
    device1  Device   master4  up     10:00:00    
    kernel1  Kernel   master4  up     10:00:00    
    ```
    You can also view detailed information for a specific protocol:
    ```
    netx(router-bird)# protocols <protocol_name>
    ```

*   **bgp neighbor**: Displays BGP neighbor status (shortcut for `show protocols` filtered for BGP).
    ```
    netx(router-bird)# bgp neighbor
    ```

## BIRD CLI

Switching between `netc` and BIRD CLI can be easily done with `birdc` command. If BIRD version 1.x is running, `birdc` and `birdc6` commands are available as
BIRD 1.x uses two separate routing processes -- see a [comparison](l3-advanced.md#bird-version-12) between versions.

```
netx# birdc
BIRD 2.0.2 ready.
bird> 

! Use exit, quit or ctrl+d to switch back to netc CLI

bird> quit
netx# 
```

BIRD CLI has several commands useful for troubleshooting and displaying info. You can use `?` to obtain context sensitive help.

```
! Obtain help in global context
netx# birdc
BIRD 2.0.2 ready.
bird> ?
quit                                           Quit the client
exit                                           Exit the client
help                                           Description of the help system
show ...                                       Show status information
dump ...                                       Dump debugging information
eval <expr>                                    Evaluate an expression

<snip>

! Obtain help in show context

bird> show ?
show status                                    Show router status
show memory                                    Show memory usage
show protocols [<protocol> | "<pattern>"]      Show routing protocols
show interfaces                                Show network interfaces
show route ...                                 Show routing table

<snip>
```

Further description can be found in BIRD [documentation](https://bird.network.cz/?get_doc&v=20&f=bird-4.html).

## BIRD version 1/2

NetX platform supports both BIRD 1.x and BIRD 2.x versions of routing daemons. The differences between these versions are outlined in the following table:

| Feature | BIRD 1.x | BIRD 2.x |
| ---     | ---      | ---      |
| Code stability | Stable | Stable / Experimental |
| Config file syntax stability | Stable | Incompatible changes can appear in future versions |
| Deployment | Critical Environments (IXPs, Core routers) | Standard Environment |
| IPv6 support | 2 separate routing processes | Single routing process |
| MPLS | no | yes |
| FlowSpec | no | yes |
| RPKI | no | yes |
| NetX default | no | yes |
 
BIRD 2 is the default version on NetX platform, and it's recommended to use. If you need to switch to BIRD 1.x, please contact NetX Support 
(support@netx.as) for additional information.

## BGP

Border Gateway Protocol (BGP) is a path vector routing protocol designed to exchange routing and reachability information among autonomous systems.
BIRD routing deamon supports rich set of BGP standards. The list of supported standards together with detailed description of BIRD BGP commands are
available [here](https://bird.network.cz/?get_doc&v=20&f=bird-6.html#ss6.3). The following examples are only a subset of basic commands used with BGP.

> [!TIP]
> See [tutorials](~/tutorials/bgp/basic-bgp.md) section for advanced config examples.

Each instance of the BGP protocol in BIRD config file corresponds to one neighboring router. Syntax for BGP protocol is the following:

```
protocol bgp [name [from template_name]] { protocol options }
```

*name* is not mandatory, but it's recommended for better troubleshooting. It's possible to set common options with a template and apply to a neighbor
with *from template_name* expression. The following example sets BGP neighbor with name MY_CUSTOMER, ASN 64500 and IP addresses to 192.0.2.1 and 
2001:db8::1. Other protocol options are left to default values. 

```
protocol bgp MY_CUSTOMER4 { 
	local as 65000;
	neighbor 192.0.2.1 as 64500; 
}

protocol bgp MY_CUSTOMER6 { 
	local as 65000;
	neighbor 2001:db8::1 as 64500; 
}
```  

## OSPF

Open Shortest Path First (OSPF) is a link state, interior gateway protocol. Two versions exist: OSPFv2 defined in [RFC 2328](https://tools.ietf.org/html/rfc2328) for IPv4 protocol and OSPFv3 defined in [RFC 5340](https://tools.ietf.org/html/rfc5340) for IPv6 protocol.
Both protocols are supported and can be configured by editing BIRD config file. The desired OSPF version can be specified by using ospf v2 or ospf v3 as a protocol type.
By default, OSPFv2 is used. The following example shows the syntax for OSPF protocol:

```
protocol ospf [v2|v3] [name] { protocol options }
```

The following configuration example enables both OSPFv2 and OSPFv3 on `ge2` interface in backbone OSPF area.

```
protocol ospf v2 OSPFv2 {
    ipv4 { export all; };
    area 0 {
        interface "ge2";
    };
}

protocol ospf v3 OSPFv3 {
    ipv6 { export all; };
    area 0 {
        interface "ge2";
    };
}
```

It is possible to verify protocols details using `show` commands in BIRD CLI. E.g.

```
! switch to BIRD CLI
netx# birdc
BIRD 2.0.2 ready.

! display all configured protocols
bird> show protocols
Name       Proto      Table      State  Since         Info
DEVICE     Device     ---        up     16:16:32.849
DIRECT     Direct     ---        up     23:03:30.775
KERNEL4    Kernel     master4    up     16:16:32.849
KERNEL6    Kernel     master6    up     16:16:32.849
OSPFv2     OSPF       master4    up     17:21:16.001  Running
OSPFv3     OSPF       master6    up     00:07:13.115  Running

! display OSPFv2 neighbors

bird> show ospf neighbors OSPFv2
OSPFv2:
Router ID   	Pri	     State     	DTime	Interface  Router IP
192.168.1.26	  1	Full/BDR  	 35.885	ge2        192.168.1.26

! go back to NETX CLI
bird> exit
netx#

BIRD allows to set a rich set of different OSPF protocol options.
