# Default configuration #

There is a default configuration to help with an initial configuration of NETX router. Any freshly installed NETX router, will start with these defaults:

* Configuration for `ge1` interface is set to obtain an address from a DHCP server 
* Configuration for `ge2` interface uses the following config:

```
IPv4 address: 192.168.1.100/24
IPv4 default gateway: 192.168.1.1
```

* SSH daemon is running on standard port 22

## Login Credentials ###

The default configuration use the following credentials:

```
admin/N3tX0559
```

The `admin` account has full configuration privileges. The `root` account password is set to null by default (login is disabled). 

> [!IMPORTANT]
> For optimum security, the default password for `admin` account should be changed before you start to configure NETX 
> router - see [User management](system/basics.md#user-management) for details.

After the first successful login, the default shell is shown:

```
# ssh 192.168.1.100 -l admin

  _   _      _    __  __
 | \ | | ___| |_  \ \/ /
 |  \| |/ _ \ __|  \  / 
 | |\  |  __/ |_   /  \ 
 |_| \_|\___|\__| /_/\_\
                      

[NetX-X1120]#  
```

The default `hostname` is set to NETX platform - `NetX-X1120` in the example. The hostname can be changed according the needs - see [Basic system settings](system/basics.md#hostname). In the rest of the documentation, `netx` hostname is used.

## Serial Console 

Serial console management is fully supported. NETX router provides two USB ports, that can be used with USB to Serial Adapter. Default baud-rate speed 
is set to 9600. The following example shows login via serial link.

```
[root@test ~]# screen /dev/ttyUSB5

NetXOS 7 (Core)
Kernel 3.10.0-693.17.1.el7.netx.x86_64 on an x86_64

netx login: 
```
