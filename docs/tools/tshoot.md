# Troubleshooting tools 

There are several troubleshooting tools incomporated in every NETX router. The standard tools, such as `ping` and 
`traceroute` are available using `netc` CLI. It is, however, possible to use any other standard troubleshooting
tools available in Linux (e.g. `tcpdump`, `tshark`, `tracepath`, `mtr`, etc.) if you switch to the standard shell using
`shell` command in global mode.

## Ping 

The `ping` and traceroute commands are available in the global context and can be adjusted by several settings. Help for the 
commands is available using `?`.

```
netx# ping ?

 <host>               - Host name or IP
 count                - number of packets
 interface            - output interface name
 interval             - set wait interval in seconds
 ipv4                 - force IPv4 protocol
 ipv6                 - force IPv6 protocol
 numeric              - do not lookup DNS names
 size                 - packet size in Bytes
 source               - source ip address

netx# ping ipv6 google.com
PING google.com(ham02s17-in-x0e.1e100.net (2a00:1450:4005:80b::200e)) 56 data bytes
64 bytes from ham02s17-in-x0e.1e100.net (2a00:1450:4005:80b::200e): icmp_seq=1 ttl=54 time=23.8 ms
64 bytes from ham02s17-in-x0e.1e100.net (2a00:1450:4005:80b::200e): icmp_seq=2 ttl=54 time=23.6 ms
64 bytes from ham02s17-in-x0e.1e100.net (2a00:1450:4005:80b::200e): icmp_seq=3 ttl=54 time=23.6 ms

--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 23.657/23.721/23.832/0.194 ms
```

## Traceroute

Similarly, the `traceroute` command is available as well.

```
netx# traceroute ?

 <host>               - Host name or IP
 interface            - output interface name
 ipv4                 - force IPv4 protocol
 ipv6                 - force IPv6 protocol
 numeric              - do not lookup DNS names
 source               - source ip address

netx# traceroute numeric netx.as
traceroute -n netx.as
traceroute to netx.as (185.62.108.110), 30 hops max, 60 byte packets
 1  185.135.134.1  0.333 ms  0.269 ms  0.213 ms
 2  185.1.25.4  0.195 ms  0.193 ms  0.238 ms
 3  147.229.252.113  1.221 ms  1.773 ms  2.272 ms
 4  147.229.252.214  1.057 ms  1.620 ms  1.797 ms
 5  185.62.108.110  0.372 ms  0.354 ms  0.310 ms
```

## Other tools

By switching to unix shell mode, several other networking troubleshooting tools are available. These include `tcpdump`,
`nmap` scanner, `mtr` and others. The following example invokes tcpdump commands to intercept all ARP traffic in VLAN 110
on port ve2.

```
! Show only ARP traffic in VLAN 110 on port ve2
netx# shell
[root@netx ~] # tcpdump -i ve2.110 -nn 'arp'
listening on ve2.110, link-type EN10MB (Ethernet), capture size 262144 bytes
16:54:57.902497 ARP, Request who-has 185.135.135.18 tell 185.135.135.2, length 28
16:54:57.986840 ARP, Request who-has 185.135.135.34 tell 185.135.135.2, length 28
16:54:57.986852 ARP, Request who-has 185.135.135.202 tell 185.135.135.2, length 28
^C
```
