# Firewall

The NetX platform provides a comprehensive firewall configuration interface based on `iptables` (for IPv4) and `ip6tables` (for IPv6). It allows you to manage tables, chains, and rules directly from the CLI, as well as use "match lists" (ipsets) for efficient matching of large sets of IP addresses or ports.

## Context

Firewall configuration is divided into IPv4 and IPv6 contexts.

**IPv4 Firewall:**
```
netx# ipv4 firewall
netx(fw4)# 
```

**IPv6 Firewall:**
```
netx# ipv6 firewall
netx(fw6)# 
```

The commands and structure are identical for both versions, with the exception of address formats.

## Match Lists (IP Sets)

Match lists (based on `ipset`) allow you to create lists of IP addresses, networks, ports, or MAC addresses and reference them in firewall rules. This is much more efficient than creating individual rules for each item.

### Managing Match Lists

To configure match lists, enter the `match-list` context:

```
netx(fw4)# match-list
netx(matchlist4)# 
```

**Create a match list:**
```
netx(matchlist4)# <name> key <type> [options]
```
*   `key <type>`: Type of the list. Common types:
    *   `hash:ip`: Set of IP addresses.
    *   `hash:net`: Set of networks (CIDR).
    *   `hash:ip,port`: Set of IP address and port pairs.
    *   `hash:mac`: Set of MAC addresses.
*   `maxelem <num>`: Maximum number of elements (default 65536).
*   `timeout <num>`: Default timeout for entries.

**Example:**
```
netx(matchlist4)# blacklist key hash:ip
```

**Add entries to a list:**
Enter the list context:
```
netx(matchlist4)# blacklist
netx(matchlist4-blacklist)# action add ip 192.0.2.1
netx(matchlist4-blacklist)# action add ip 198.51.100.0/24
```

**Show match lists:**
```
netx(matchlist4)# show match-list
```

## Tables and Chains

The firewall is organized into standard tables (`filter`, `nat`, `mangle`, `raw`) and chains. You can manage rules within these chains.

### Managing Tables

Enter the `table` context and select a table (e.g., `filter`, `nat`):
```
netx(fw4)# table filter
```

### Managing Chains

Within a table, you can select an existing chain (like `INPUT`, `FORWARD`, `OUTPUT`) or create a custom chain.

**Select a chain:**
```
netx(fw4)# table filter chain INPUT
netx(fw4-INPUT)# 
```

**Create a custom chain:**
```
netx(fw4)# table filter chain MY_CHAIN
```

### Managing Rules

Rules are added to chains using the `action` command.

**Syntax:**
```
action <target> [options]
```

**Common Options:**
*   `src <ip/net>`: Source IP/Network.
*   `dst <ip/net>`: Destination IP/Network.
*   `proto <protocol>`: Protocol (tcp, udp, icmp, etc.).
*   `sport <port>`: Source port.
*   `dport <port>`: Destination port.
*   `in <interface>`: Input interface.
*   `out <interface>`: Output interface.
*   `match-list <name>`: Match against a match list.
*   `comment <string>`: Rule comment.

**Targets:**
*   `ACCEPT`: Accept the packet.
*   `DROP`: Drop the packet.
*   `REJECT`: Reject the packet.
*   `LOG`: Log the packet.
*   `DNAT`: Destination NAT (in `nat` table).
*   `SNAT`: Source NAT (in `nat` table).
*   `MASQUERADE`: Masquerade (in `nat` table).
*   Custom chain name: Jump to a custom chain.

**Examples:**

1.  **Allow SSH from a specific subnet:**
    ```
    netx(fw4-INPUT)# action ACCEPT src 192.168.1.0/24 proto tcp dport 22
    ```

2.  **Drop traffic from a blacklist:**
    ```
    netx(fw4-INPUT)# action DROP match-list blacklist
    ```

3.  **Port Forwarding (DNAT):**
    ```
    netx(fw4)# table nat chain PREROUTING
    netx(fw4-PREROUTING)# action DNAT proto tcp dport 8080 to-destination 192.168.1.50:80
    ```

4.  **Masquerade (NAT):**
    ```
    netx(fw4)# table nat chain POSTROUTING
    netx(fw4-POSTROUTING)# action MASQUERADE out tge1
    ```

## Custom Scripts

For complex firewall logic that is difficult to express via the CLI, you can use custom shell scripts. These scripts are executed to apply firewall rules directly using `iptables` commands.

> [!TIP]
> For complex configurations, it is highly recommended to use the `timeout` option when applying scripts. This ensures that if the new rules cause you to lose connectivity to the router, the changes will be automatically reverted after the specified time, preventing a permanent lockout.

**Set the script file:**
You can specify the name of the script file to use. If you provide a filename without a path, it will be created in `/etc/netc/firewall/` by default. You can also provide a full absolute path.

```
netx(fw4)# custom-script ipv4-custom-firewall
```

**Edit the script:**
```
netx(fw4)# custom-script edit
```
This opens an editor where you can write your script.

**Apply the script with safety timeout:**
It is recommended to apply changes with a timeout (in seconds). If you do not confirm the changes within this period, the previous configuration is restored.

```
netx(fw4)# custom-script apply timeout 60
```

**Confirm the changes:**
If the configuration works as expected, you must confirm it to make it permanent.

```
netx(fw4)# custom-script confirm
```

**Show the script:**
```
netx(fw4)# show custom-script
```

## Advanced Rule Options

The firewall supports a wide range of options for fine-tuning rules.

### Connection Tracking

You can match packets based on their connection state using the `state` option.

*   `state <state-list>`: Comma-separated list of states (NEW, ESTABLISHED, RELATED, INVALID, UNTRACKED).
*   `not-state <state-list>`: Match if the packet is NOT in the specified states.

**Example: Allow established connections**
```
netx(fw4-INPUT)# action ACCEPT state ESTABLISHED,RELATED
```

### Logging

You can log packets that match a rule. It is often useful to limit the rate of logging to avoid flooding the logs.

*   `log-prefix <string>`: Prefix added to the log message.
*   `log-amount <rate>`: Limit the logging rate (e.g., `5/min`, `10/sec`).

**Example: Log dropped packets with a limit**
```
netx(fw4-INPUT)# action LOG log-prefix "DROP: " log-amount 5/min
```

### Packet Marking

You can set internal marks or DSCP values on packets, which can be used for Policy Based Routing (PBR) or QoS.

*   `set-mark <value[/mask]>`: Set the firewall mark (e.g., `0x1`, `0x10/0xf0`).
*   `set-dscp <value>`: Set the DSCP value (e.g., `0x2e`).

**Example: Mark packets for QoS**
```
netx(fw4-PREROUTING)# action ACCEPT set-mark 0x10
```

### TCP Flags

You can match specific TCP flags.

*   `tcp-flags <mask,comp>`: Match TCP flags. The first part is the mask (flags to check), the second is the flags that must be set.

**Example: Match SYN packets (new connections)**
```
netx(fw4-INPUT)# action ACCEPT proto tcp tcp-flags SYN,RST,ACK,FIN,SYN
```

### Other Options

*   `length <range>`: Match packet length (e.g., `100:200`).
*   `limit <rate>`: Rate limit matches (similar to log-amount but for any action).
*   `reject-with <type>`: When using REJECT target, specify the ICMP error type (e.g., `icmp-host-unreachable`).

## Showing Configuration

You can view the current firewall configuration using the `show` command.

**Show all firewall rules:**
```
netx# show ipv4 firewall
```

**Show a specific table:**
```
netx# show ipv4 firewall table filter
```

**Show a specific chain:**
```
netx# show ipv4 firewall table filter chain INPUT
```

