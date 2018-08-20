# Basic system setting

Setting basic system information is done in `system` context. This context allows to set hostname, clock, DNS, NTP, users, etc.

## System info

The basic system info is available using `show system` command. The command outputs info about NetX platform, `netc` version, 
NetXOS version, uptime and current power consumption (power consumption info is not available for cloud platform). The command
prints an out-of-band management IP address as well -- see [Out of band management](basics.md#out-of-band-management) for
details how to set the address. Example of the command output. 

```
netx# show system 
Platform:             NetX-X1120
NetX OS version:      NetXOS release 7.4.1708 (Core) 
Netc version:         1.12 
Kernel version:       3.10.0-693.17.1.el7.netx.x86_64
Uptime:               up 9 weeks, 5 days, 21 hours, 20 minutes
Power Consumption:    46 W
Service Module IP:    192.168.1.1/24
```

> [!NOTE]
> `netc` uses `X.XX` versioning scheme for a stable build. If you enable devel repository, new package is built with every commit to `netc` git. In this case,
> the versioning scheme is changed to `X.XX.C.abrv`, e.g. `1.9.53.gb653e32` , where `C` is number of commits since stable and `abrv` is an abbreviated 
> object name for the commit itself.  

## Hostname

To change the hostname, run `system hostname` command with the desired hostname or use `hostname` command in the system context.

```
netx# system hostname test-rt
test-rt# system hostname netx
netx#
```

## DNS

Setting search domain and addresses of DNS serveres in the `system` context is done using `name-server` and `domain-lookup` commands. 

```
netx# system domain-lookup domain.com 
netx# system name-server 8.8.8.8
netx# system name-server 1.1.1.1

! You can use show command to verify the settings
netx# show system domain-lookup
domain.com
netx# show system name-server
8.8.8.8
1.1.1.1
```

## Clock, timezone

Setting timezone and clock information is possible using the `clock` command in the `system` context. `show system clock` command can be used
to verify the settings.

```
netx# show system clock
      Local time: Wed 2017-05-03 15:22:31 UTC
  Universal time: Wed 2017-05-03 15:22:31 UTC
        RTC time: Wed 2017-05-03 15:22:53
       Time zone: UTC (UTC, +0000)
NTP synchronized: no
 RTC in local TZ: no
      DST active: n/a

netx# system clock set 2017-01-10 16:22:13 

! It is possible to use <TAB> completion to find the correct timezone.
netx# clock timezone Europe/Prague
```

## NTP

NTP settings is done via `system ntp` command. It is possible to set IP address or domain name of NTP server. The 
default configuration use NTP servers `ntp1.netx.as` and `ntp2.netx.as`. The `show system clock` command can be used
to verify the settings. 

```
netx# system ntp ntp1.netx.as
      Local time: Wed 2017-05-03 18:22:55 CEST
  Universal time: Wed 2017-05-03 16:22:55 UTC
        RTC time: Wed 2017-05-03 16:23:17
       Time zone: Europe/Prague (CEST, +0200)
NTP synchronized: yes
 RTC in local TZ: no
      DST active: yes
 Last DST change: DST began at
                  Sun 2017-03-26 01:59:59 CET
                  Sun 2017-03-26 03:00:00 CEST
 Next DST change: DST ends (the clock jumps one hour backwards) at
                  Sun 2017-10-29 02:59:59 CEST
                  Sun 2017-10-29 02:00:00 CET
```

More detailed information can be obtained by issuing a `show system ntp` command.
The command displays detailed information about connected servers, their operational status, etc.

```
netx# show system ntp

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*147.229.3.100   195.113.144.238  2 u   42  128  377    0.267    0.213   0.024
```

The columns meaning is the following:

* **remote** : the remote server that is used for clock synchronization. The single character next to the remote server indicates whether 
  the remote server is used for time synchronization. Possible values are:
    * __*__ : current time source used for clock synchronization
    * __#__ : source selected, an alternative backup. This is only shown if more than 10 remote servers are configured
    * __+__ : source selected, if the current time source (`*`) is discarded, this is a candidate as a new best source
    * __o__ : source selected, Pulse Per Second (PPS) is used
    * __x__ : source discarded by the intersection algorithm
    * __.__ : source discarded by the intersection algorithm
    * __-__ : source discarded by cluster algorithm
    * __blank__ : source discarded as not valid, the reason can be uncreachability, high stratum, etc.

* **refid** - the upstream stratum to the remote server. For stratum 1 servers, this will be the stratum 0 source
* **st** - the stratum level, 0 through 16.
* **t** - the type of connection. The most common values are:
    * **u** : unicast
    * **b** : broadcast or multicast
    * **l** : local reference clock 
* **when** : the last time (seconds) when the server was queried for the time. 
* **poll** : how often the server is queried for the time
* **reach** : success and failutre rate of communicating with the remote server. 8-bit left shift octal value. Success means the bit is set, failure means the bit is not set. 377 is the highest value (all attempts successful).
* **delay** : round trip time (RTT) to the remote server (millisecods)
* **offset** : how far off are the clock from the reported time on the remote server (milliseconds). It can be possitive or negative. 
* **jitter** : the root mean squared deviation of offsets (milliseconds).

## User management

The default username in NETX routers is `admin` with `netc` set as the default shell. Additional users can be added in the `system` context
using `user` command. 

Adding a user via `user <username>` command

```
! Add user 'test'
netx# system user test
netx(user-test)# 
```

Password can be changed via `password` command. A new password can be specified directly as a string parameter of the `password` command or
interactively if `ENTER` is pressed after `password` command. 

```
! Set the password for the user
netx(user-test)# password
Changing password for user test-user.
New password: 
Retype new password:
passwd: all authentication tokens updated successfully.
```

It is possible to set encrypted password directly using `crypt` keyword in `user` context. The `crypt` command expect input format
compatible with crypt glibc function.
 
User's login shell can be changed according the needs. The default login shell is `netc` shell, but if e.g., bash shell is required
it is possible to change it via `login-shell` command.

```
! Set user's login shell to bash
netx(user-test)# login-shell bash
```

The user can be removed via `no user <username>` command.

```
! Remove user 'test'
netx(system)# no user test
```

## Password recovery

If password for the `admin` account is forgotten, it is possible to start password recovery procedure by issuing the following steps:

1. Connect __`ge1`__ and __`ge2`__ interfaces with straight through Ethernet cable
2. Reboot NETX router
3. After the reboot, the `admin` credentials are set to default - `admin/N3tX0559` in running config
4. Log in and change the password using `system user admin password` command
5. Save the password using `copy running-config startup-config` command
6. Disconnect the cable between __`ge1`__ and __`ge2`__ interfaces
7. Reboot NETX router

> [!NOTE] 
> The rest of the `startup-configuration` is not changed. If you need to put NETX router to default configuration,
> run `shell` command following with `rm /etc/netc/startup-config` after step `3` and then continue with step `6`.

## Default Editor

Parts of NETX configuration, e.g., bird or firewall (iptables) configs, can be edited by an editor. The default editor is `vim`,
however, different editor can be set as well using the `system editor` command.

```
! list available editors
netx# system editor ?

 <str>                - editor name
 joe                  
 mcedit               
 nano                 
 vi                   
 vim                  

! change the default editor to nano
netx# system editor nano

! revert back to vim
netx# no system editor nano
```

## Out-of-band management
The out-of-band management is implemented using Intelligent Platform Management Interface (IPMI) and provides management and 
monitoring capabilities independently of the NETX system. The configuration is available in `system` context using `service-module` 
command. 

```
netx# show system service-module ?

 <cr>                 
 factory-default      - Load default configuration to service module
 gw                   - Service interface IPv4 Gateway
 ip                   - Service IPv4 interface
 user                 - Service user list
```

Setting up management IP address and gateway:

```
netx# system service-module ip 192.168.1.1/24
netx# system service-module gw 192.168.1.254
```

Setting up user `new_admin` with a top secret password: 

```
netx# system service-module user new_admin password secretpassword
```

Management web interface is available at `https://<service-module ip>`. The settings can be 
shown using `show system service-module` command.

```
netx# show system service-module 
Power Consumption:    44 W
PS1:                  OK
PS2:                  OK
Fan1:                 5400 RPM
Fan2:                 5600 RPM
Fan3:                 5700 RPM
CPU:                  60 C
System:               35 C
Peripheral:           38 C
DIMMA1:               29 C
DIMMB1:               31 C
Service Module IP:    192.168.1.1/24
Service Module GW:    192.168.1.254
Service Module MAC:   ac:1f:6b:2e:e7:28
```

There are separate commands to show just info about power supplies, fans and CPU temperatures. E.g.

```
netx# show system power 
Power Consumption:    45 W
PS1:                  OK
PS2:                  OK

netx# show system fan 
Fan1:                 5400 RPM
Fan2:                 5700 RPM
Fan3:                 5600 RPM

netx# show system temperature 
CPU:                  59 C
System:               35 C
Peripheral:           38 C
DIMMA1:               28 C
DIMMB1:               31 C
```

The list of usernames can be shown via `show system service-module user`. E.g.:

```
netx(config)# show service-module user
netx new_admin
```

