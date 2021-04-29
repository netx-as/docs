# Default configuration

There is a default configuration to help with an initial configuration of NetX router. Any freshly installed NetX router, will start with these defaults:

* Configuration for `ge1` (`tge1` on X12 series) interface is set to obtain an address from a DHCP server 
* Configuration for `ge2` (`tge2` on X12 series) interface uses the following config:

```
IPv4 address: 192.168.1.100/24
IPv4 default gateway: 192.168.1.1
```

* SSH daemon is running on standard port 22

## Login Credentials

The default configuration use the following credentials:

```
admin/N3tX0559
```

The `admin` account has full configuration privileges. The `root` account password is set to null by default (login is disabled). 

> [!IMPORTANT]
> For optimum security, the default password for `admin` account should be changed before you start to configure NetX
> router - see [User management](~/docs/system/basics.md#user-management) for details.

After the first successful login, the default shell is shown:

```
# ssh 192.168.1.100 -l admin

  _   _      _    __  __
 | \ | | ___| |_  \ \/ /
 |  \| |/ _ \ __|  \  /
 | |\  |  __/ |_   /  \
 |_| \_|\___|\__| /_/\_\

 Docs:    https://docs.netx.as
 Support: support@netx.as


[NetX-X1120]#
```

The default `hostname` is set according to NetX platform - `NetX-X1120` in the example. The hostname can be changed according the
needs - see [Basic system settings](~/docs/system/basics.md#hostname). In the rest of the documentation, `netx` hostname is used.

## Out of band management

NetX provides dedicated port for out of band management (OoB). The OoB port allows to log to the web-based interface and remotly reboot,
shutdown, power on/off the device or remotely access the terminal. The OoB port is truly independent of the NetX system's CPU, firmware
and operating system. Default IP settings for OoB port is following:

```
IPv4 address: 192.168.1.101/24
IPv4 default gateway: 192.168.1.1
```

To access the web-based system, it is possible to open a standard web browser and navigate to `https://192.168.1.101` web page.
Default user credential for login is the following:

```
netx/N3tX0559
```

> [!IMPORTANT]
> For optimum security, the default `admin` account is disabled. The password for `netx` account should be changed before you start to
> configure NetX router - see [OoB configuration](~/docs/system/basics.md#out-of-band-management) for details.

## Serial Console 

Serial console management is fully supported. NetX router provides two USB ports, that can be used with USB to Serial Adapter. Default baud-rate speed 
is set to 9600. The following example shows login via serial link.

```
[root@test ~]# screen /dev/ttyUSB5

NetXOS 7 (Core)
Kernel 3.10.0-693.17.1.el7.netx.x86_64 on an x86_64

netx login: 
```
