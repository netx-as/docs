# IP blacklist

This tutorial provides step by step instruction how to configure and maintain a blacklist that will be used 
for dropping forwarded traffic from a specific source address or networks. Every entry will be hold in the 
blacklist for 1 hour. If the existing entry is added again the timeout will reset and starts again from beginning. 

1. Create a match-list. The match-list is named `BLACKLIST` will contain IP addresses or networks that will 
be blacklisted.

```
netx# ipv4 firewall match-list BLACKLIST timeout 3600
netx(matchlist4-BLACKLIST)# exit
```

2. Create a firewall rule in build-in `FORWARD` chain that and tie drop action with match-list created in the previous step.

```
netx# ipv4 firewall table filter chain FORWARD
netx(fw4-filter-FORWARD)# action DROP match-list BLACKLIST match-field src
```

3. Add entries (ip addresses 1.1.1.3, 1.1.1.4) to the match-list via REST API. It is possible to add the IP address via 
`rest-netc-client` or cURL clients.

```
rest-netc-client -p -A SET -O net=1.1.1.3 ipv4 firewall match-list BLACKLIST action match
```

or via cURL

```
curl --data '{"Options":{"net":["1.1.1.4"]},"Actions":["SET"]}' \
-X POST \
--user user:password \
https://<netx-address>/api/ipv4/firewall/match-list/BLACKLIST/action/match 
```

4. Watch and monitor entries and matched number of dropped bytes and packets for the specific addresses

```
netc# monitor ipv4 firewall match-list BLACKLIST 

 12:27:00   delay: 1 s
----------------------------------------------------------------
Match-list name:     BLACKLIST
Key(s):              net
Number of entries:   2
Referenced:          1
Size in memory:      1336 B
Max elements:        65536
Default timeout:     3600 s
Members:
1.1.1.3 timeout 3202 packets 0 bytes 0
1.1.1.4 timeout 3405 packets 0 bytes 0
                                                                                                                                                         
----------------------------------------------------------------
```

6. Delete an entry from the match-list can be done via UNSET action.

```
curl --data '{"Options":{"net":["1.1.1.3"]},"Actions":["UNSET"]}' \
-X POST \
--user user:password \
https://<netx-address>/api/ipv4/firewall/match-list/BLACKLIST/action/match 
```

## IP + port blacklist
This example is similar to previous one, but both IP address and port number are used for blacklisting. 

1. Create a match-list named `BLACKLIST2` that matches both IP address and port numbers.

```
netc# ipv4 firewall match-list BLACKLIST2 key net-port timeout 3600
```

2. Create a firewall rule and tie it with the match-list. The first match field references to 
the source ip/net, the second one to the destination port

```
netc(fw4-filter-FORWARD)# action DROP match-list BLACKLIST2 match-field src match-field dst
```

3. Use REST API to install an entry

```
curl --data '{"Options":{"net":["1.1.1.4"], "port":[80], "protocol":["tcp"]},"Actions":["SET"]}' \
-X POST \
--user user:password \
https://<netx-address>/api/ipv4/firewall/match-list/BLACKLIST2/action/match 
```
