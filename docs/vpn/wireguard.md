# WireGuard

> [!TIP]
> Check also the folowing tutorials:
> * [WireGuard: Set up basic site-to-site VPN](~/tutorials/vpn/wireguard.md)

WireGuard is an simple yet fast and modern VPN that utilizes state-of-the-art cryptography. WireGuard is designed as
a general purpose VPN and fits for many different circumstances. Initially released for the Linux kernel, it is now
cross-platform (Windows, macOS, BSD, iOS, Android) and widely deployable.

WireGuard encrypts and encapsulates traffic into UDP packets. WireGuard does not handle key distribution or authentication,
leaving that to other tools.

### Commands and context

There are several commands that can help with setting up a WireGuard tunnel. The commands are available in WireGuard
interface context that can be created using `interface wg<number>` command. The following example shows how to create 
WireGuard interface `wg0`.

```
netx# interface wg0
netx(if-wg0)# <command>
```

#### listen-port

Change the listening port for WireGuard tunnel.

##### Syntax

`listen-port <port>`

##### Default value

The default port is set to standard WireGuard port number `51820`.

---

#### peer

Switch to interactive editing mode, where it is possible to configured WireGuard peers.
Syntax for the configuration file is the same as WireGuard [config file](https://man7.org/linux/man-pages/man8/wg.8.html#CONFIGURATION_FILE_FORMAT).


##### Syntax

`peer`

See [WireGuard: set up basic VPN](~/tutorials/vpn/wireguard.md) tutorial for further info.

##### show

The `show peer` command in the WireGuard interface context displayes the configured peers,
last communication, number of transferred packets and bytes and other information.

```
netx# show interface wg0 peer
peer: ukhouOiMAMwpVqCFITVjifatTlwhYgmQm3am0zvL11E=
  endpoint: 100.90.110.27:51820
  allowed ips: 192.168.2.2/32, 10.0.2.0/24
  latest handshake: 35 seconds ago
  transfer: 1.18 KiB received, 1.09 KiB sent
```

---

#### public-key

Displays the public key for an WireGuard interface.

##### Example

```
netx# show public-key
ukhouOiMAMwpVqCFITVjifatTlwhYgmQm3am0zvL11E= 
```

---
