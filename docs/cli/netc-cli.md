# CLI

`netc` is a command line interface for NETX products, with the goals to simplify and automate the networking configuration process.
It is possible to use `netc` in two basic modes:

* configuration shell: `netc` runs as a configuration shell, similarly to Cisco/Juniper or Mikrotik shells. It uses standard `readline` library, 
thus all standard shortcuts are available. This is the default mode that is available after login.
* unix command: `netc` operates directly in the unix shell (e.g., `bash`). Completion support is available to allow you to complete commands and their 
arguments easily.

## Netc shell

The built-in CLI is ready to use after you login as `admin` or as a user with `netc` login shell. You can use `?` to display list of available 
commands in the active context.   

``` 
netx# ?

 birdc                - switch to internal bird CLI
 birdc6               - switch to internal bird CLI for IPv6
 copy                 - copy configuration command
 interface            - network interfaces
 ipv4                 - ip address configuration
 ipv6                 - set ipv6
 monitor              - Monitor information
 no                   - negate command
 ping                 - ping commnad
 router               - set router
 shell                - switch to unix shell enviroment
 show                 - show information
 system               - Set system's basic configuration
 traffic-manager      - Traffic manager options

 <snip>
``` 

The question mark can also be used to provide help for partially entered command. The following example shows all 
options beginning with `tg` prefix in the interface command (two 10 Gbps interfaces `tge1` and `tge2` are available). 

``` 
netx# interface tg?

 tge1                 
 tge2                 

``` 

To save keystrokes when typing command strings, you can use `TAB` command. 

```
netx# inter<TAB>
netx# interface 
```

Double `TAB` key shortcut can be used similarly to `?` to display available options to complete the commnad. 

```
netx# interface tge<TAB><TAB>
tge1  tge2  
```

### Context switching
`netc` uses different configuration contexts for some commands. For example, if you enter the following configuration,
all commands will be applied to `tge1` interface.

```
netx# interface tge1 
netx(if-tge1)# 
netx(if-tge1)# ipv4 address 192.0.2.1/24
```

`exit` command is used for returning back to the main context. 

```
netx(if-tge1)# exit
netx# 
```

### Logout
You can quit the configuration shell by typing `exit` command or by pressing `CTRL+D`.

```
 netx# exit
 Goodbye...
```

If `netc` is user's default shell, the user will be logged out. 

## Unix shell

It is possible to configure NETX router via `netc` even if the user uses a different login shell, e.g., `bash`. `netc` can operate directly from unix 
command line. The only difference is the context switching. A command must be entered including the whole context, e.g.:

```
# netc interface tge1 ipv4 address 1.1.1.1/24
```

The unix command mode uses completion via `TAB` key and completion suggestions are also available. 

```
# netc interface t<TAB>
# netc interface tge<TAB><TAB>
tge1  tge2
```

It is possible to use `?` to lists all valid completions. The following example invokes `netc` command with the `?` to list all available 10 Gbps interfaces.

```
# netc interface tge?<enter>

 tge1                 
 tge2           
```

It is possible to invoke `netc` command and start the `netc` configuration shell from the standard unix shell. 

```
 [root@netx ~]# netc
 netx#
```

The opossite direction (from netc shell to e.g., bash) is available as well using `shell` command.

```
netx# shell
[root@netx ~]# 
```
