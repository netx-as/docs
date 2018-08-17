# System configuration files

`netc` uses startup and running configuration. The running configuration is the configuration that is actually loaded and being used by the `netc`.
The startup configuration is saved in the `/etc/netc/startup-config` file. `netc` reads and loads the startup configuration upon a boot or a restart.
It is possible to save the running configuration to the disk by issuing `copy` command e.g.: 

```
netx# copy running-config startup-config 
Configuration saved to /etc/netc/startup-config
```

It is possible to specified the name of the config file: 

```
netx# copy running-config myconfig1 
Configuration saved to /etc/netc/myconfig1
```

Other commands that can be used as well are `write memory` and `save`. These commands save the output always to the file
startup-config. E.g.,

```
netx# save
Configuration saved to /etc/netc/startup-config
```

Using the `copy` command, the configuration can be loaded from the config file to replace the current running configuration.

```
netx# copy myconfig1 running-config
```

## Display config

The current running configuration can be displayed by typing `show running-config` command. The `!` character is used only for 
better visibility and separation of different config parts. It is possible to used lines with the `!` for comments in the 
configuration file. 

```
netx# show running-config
system
  hostname netx
!
  name-server 8.8.8.8
!
  ntp server ntp1.netx.as
!
   user admin
     admin crypt <ommited>
!
!
interface ve1
  ipv4 address 100.90.110.11/24
!
ipv4 route 0.0.0.0/0 100.90.110.1
!
!
<snip>
```

The command `show startup-config` can be used to display the saved startup configuration.

```
netx# show startup-config
!
! Config file created by netc at 2018-02-13 21:53:04
!
system
system hostname netx
!
system name-server 8.8.8.8
!
system ntp server ntp1.netx.as
!
system user admin
system user admin crypt <ommited>
!
!
interface ve1
interface ve1 ipv4 address 100.90.110.11/24
!
ipv4 route 0.0.0.0/0 100.90.110.1
!
!
<snip>
```

> [!TIP]
> If the configuration shell is switched into a configuration context the `show this` command displays only the relevant part 
> of the configuration in the appropriate context:

```
netx# interface bond0.111
netx(if-bond0.111)# show this 
 ipv4 address 100.90.111.5/24
 ipv6 address 2001:db8:111::4/64
```

Many configuration options can be displayed by using the `show` command. E.g.: 

```
netx# show interface 
INTERFACE       STATE          RX                    TX
                          b/s      p/s          b/s      p/s
ge1           A 1G-FD     4.2k     8.9          0.0      0.0  
ge2              down     0.0      0.0          0.0      0.0  
tge3           10G-FD     4.2k     8.8          0.0      0.0  
tge4            1G-FD     0.0      0.0          0.0      0.0  

```

Please consult a specific configuration section to get detailed information about show command options and outputs. 

