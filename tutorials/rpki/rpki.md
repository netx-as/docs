# RPKI 

Resource Public Key Infrastructure (RPKI) is designed to secure internet routing infrastructure. RPKI provides a way to perform Route Origin Validation. RPKI can be used by the legitimate holders of the resources to control the operation of Internet routing protocols to prevent route hijacking and other attacks. It is used to secure the Border Gateway protocol (BGP).

RPKI validator is used to download all of the certificates and ROAs in their repositories to validate the signatures. Validator then can feed the validated information to hardware routers as well as software solutions like BIRD.  Next example shows Routinator as RPKI Validator together with BIRD routing daemon. For more information check the BIRD [documentation](https://bird.network.cz/?get_doc&v=20&f=bird-6.html#ss6.14).

RPKI configuration example in BIRD routing daemon:

1. Start a RPKI validator (Routinator) or use a `rpki.netx.as` on port `3323` as validator.

2. Edit BIRD configuration file:
```
netx# router bird edit
```
3. Add ROA table and RPKI protocol to BIRD config:

```	
roa4 table t_roa;

protocol rpki rpki1 {
  roa4 { table t_roa; };
  remote “rpki.netx.as” port 3323;
  retry keep 90;
  refresh keep 900;
  expire keep 172800;
}
```

4. Add filter to reject ROA invalid routes:

```
filter peer_in_v4 {
        if (roa_check(t_roa, net,  bgp_path.last_nonaggregated ) = ROA_INVALID) then
        {
                reject;
        }
        accept;
}
```

