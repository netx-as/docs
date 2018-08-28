# Firewall 

This tutorial will use NETX API to create a custom firewall chain, add rules into it and remove the chain from firewall. 
We will use [rest-netc-client](~/docs/api/api.md#demo-client) in this tutorial, but it is possible to use cURL or any other HTTP client.

* create custom chain `MYCHAIN`

```
rest-netc-client -p -A SET ip firewall table filter chain MYCHAIN
```

* Add rule permiting tcp traffic from `10.10.10.0/24` to port 80

```
rest-netc-client -p -A SET  -O src=10.10.10.0/24,dport=80,proto=tcp ipv4 firewall table filter chain MYCHAIN action ACCEPT
```

* List of the rules in the chain.

```
rest-netc-client -p -A GET ipv4 firewall table filter chain MYCHAIN action

<snip>

  'SetValues' => [
                   'ACCEPT'
  ],
  'AllowShow' => 0,
  'SetOptions' => [
      {
        'proto' => [
                     'tcp'
                   ],
        'src' => [
                   '10.10.10.0/24'
                 ],
        'id' => [
                  '1'
                ],
        'dport' => [
                     '80'
                   ]
      }
  ],

<snip>

```

* Delete the firewall rule according the rule id.

```
rest-netc-client -p -A UNSET -O id=1 ipv4 firewall table filter chain MYCHAIN action ACCEPT
```

* Delete the entire chain

```
rest-netc-client -p -A UNSET ipv4 firewall table filter chain MYCHAIN
```
