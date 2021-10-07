# DDoS Guard

DDoS Guard is a built-in NetX component for ddos attacks detection and mitigation. Core of the DDoS Guard is implemented as an iptables kernel module.
It is divided into two parts - detection and mitigation called filtration.

Detection is done by counting the number of packets per second (pps) and bytes per second (bps) going through the system. If threshold is exceeded, the algorithm starts to go through the configured evaluation items e.g. source port, destination ip address, etc. These items are then evaluated and the final filtration rule is created. There are several parameters which are affecting the detection phase. We will go through these parameters in further sections.

Mitigation phase starts after the filtration rule is created. There are several actions that can be taken. DDoS Guard can apply this filtration rule and filter packets internally before it hits the system. Another option is to use bgp flowspec to propagate filtering rules into the network to mitigate the effects of a DDoS attack. Each filtration rule has a timeout. This timeout is started after the traffic is below the threshold.

Configuration is done in two places. First, the firewall rule should be configured (action DDOSGUARD) where the user defines which traffic is forwarded to the DDoS Guard. Second, the ddos-guard context which provides additional configuration. The example section below further explains this in concrete examples.

### Context

It is possible to switch to the DDoS Guard context using `ddos-guard` command.

```
netx# ddos-guard
netx(ddg)# <command>
```

### Commands

The following commands are available in ddos-guard context.

#### enable

Enable DDoS Guard engine.

##### Syntax

`enable`

##### Default value

DDoS Guard is disabled by default.

---

#### log-level

Logging level severity option. There is a option to chose between `info` and `debug` log severity.

##### Syntax

`log-level <info | debug>`

##### Default value

If log-level is not provided, `log-level info` is a default value.

---

## Configuring BGP Flowspec Reporting

Basic bgp configuration used for filter reporting using bgp flowspec.
It is possible to switch to the bgp context using `bgp` command. 

### Context

`bgp` command has own subcontext. It is possible to switch to the subcontext using the following command.

```
netx# ddos-guard bgp
netx(ddg-bgp)#
```

---

#### as

BGP autonomous system configuration.

##### Syntax

`as <number>`

---

#### router-id

Router local identification number.

##### Syntax

`router-id <IPv4Address>`

---

#### neighbor-address

Neighbor router IP address.

##### Syntax

`neighbor-address <IPv4Address>|<IPv6Address>`

---

#### neighbor-as

Neighbor router autonomous system number.

##### Syntax

`neighbor-as <number>`

---

## Configuring Rule

### Context

`rule` command has own subcontext. It is possible to switch to the subcontext using the following command.

```
netx# ddos-guard rule <rule-name>
netx(ddg-rulename)#
```

---

#### template

DDoS Guard template configuration. Rule inherits configuration from a template. If parts of configuration are in conflict, the rule configuration is superior to template configuration.

##### Syntax

`template <string>`

---

#### threshold

As described above, threshold is a crucial parameter which starts the detection process. There are several ways to configure the threshold. 
1. Based on baseline - The recommended way is to compute the threshold automatically based on the baseline. Baseline represents average traffic computed from history. Baseline is then multiplied by a coefficient called baseline-derived which results in threshold. Baseline-derived is three by default (can be changed), which means that traffic must be three times bigger than the average to start the detection phase.
2. Manually configured thresholds - Thresholds can be also configured manually. This is not recommended unless you have a precise knowledge of the affected network and traffic. The recommended way to use a manual threshold is to combine it with configuration based on the baseline. In this case the configured threshold acts as the maximal threshold. It means, when this threshold is exceeded the detection starts regardless of the threshold based on baseline. For example, this can be used as a last protection before the link is saturated or some systems are overloaded.
3. Manually configured minimal thresholds - This parameter can be configured in combination with baseline based threshold configuration. It means that the threshold computed by baseline must be at least the minimal threshold.

Threshold configuration contains several options for detailed setting of the threshold.

##### Syntax

`threshold <opts>`

---

### Threshold options

#### threshold pps

Threshold packets per second. In case of an active baseline based threshold calculation pps is used as maximal packet threshold.

##### Syntax

`pps <num>[<.num>]<suffix>`


##### Example

`pps 20k`

---

#### threshold bps

Threshold bytes per second. In case of an active baseline based threshold calculation bps is used as maximal bytes threshold.

##### Syntax

`bps <num>[<.num>]<suffix>`


##### Example

`bps 100M`

---

#### threshold pps-min

Threshold minimal packets per second. In case of an active baseline based threshold calculation pps-min is used as a minimal packet threshold.

##### Syntax

`pps-min <num>[<.num>]<suffix>`


##### Example

`pps-min 5k`

---

#### threshold bps-min

Threshold minimal bytes per second. In case of an active baseline based threshold calculation bps-min is used as a minimal bytes threshold.

##### Syntax

`bps-min <num>[<.num>]<suffix>`


##### Example

`bps-min 25M`

---

#### threshold pps-baseline-derived

Coefficient which is multiplied by baseline to get the current threshold. Baseline based threshold computation is enabled for packet per seconds by configuring this parameter.

##### Syntax

`pps-baseline-derived <num>>`


##### Example

`pps-baseline-derived 3`

---

#### threshold bps-baseline-derived

Coefficient which is multiplied by baseline to get the current threshold. Baseline based threshold computation is enabled for bytes per seconds by configuring this parameter.

##### Syntax

`bps-baseline-derived <num>`


##### Example

`bps-baseline-derived 5`

---

#### filter-timeout

Timeout in seconds after which the filtering rule is removed. This timeout is started only when the filtering traffic is under the threshold. 

##### Syntax

`filter-timeout <number>`

##### Default value

Filter timeout default value is set to 60 seconds.

---

#### baseline-coefficient

Baseline coefficient number represents time range from which is the baseline computed. 

##### Syntax

`baseline-coefficient <number>`

##### Default value

Default baseline coefficient is 300 seconds (last 5 minutes).

---

#### pass-action

Action applied to packets not matched by any filter. These are the packets matched by the firewall rule and analyzed by DDoS Guard.

##### Syntax

`pass-action <CONTINUE>|<ACCEPT>|<RETURN>|<DROP>`

##### Default value

Default `pass-action` is set to `CONTINUE`.

---

#### filter-action

Action applied to packets matched by a found filter.

##### Syntax

`filter-action <CONTINUE>|<ACCEPT>|<RETURN>|<DROP>`

##### Default value

Default `filter-action` is set to `CONTINUE`.

---

#### eval-step-msecs

Evaluation time between algorithm steps (time between checking the traffic against threshold or matching the next evaluation item). Evaluation time is configured in milliseconds.

##### Syntax

`eval-step-msecs <number>`

##### Default value

Default evaluation time is set to 1000 miliseconds (1 second).

---

#### report-mail

Email address used for reporting. More than one email address can be configured. Report alerts are sent on the start and end of the DDoS attack.

##### Syntax

`report-mail <string>`

---

#### report-bgp-flowspec

Enables reporting via BGP flowspec.

##### Syntax

`report-bgp-flowspec`

---

#### description

Rule description.

##### Syntax

`description <string>`

---

#### eval-items

Items which should be searched when detecting the DDoS attack. Items are searched in the specified order.

List of available items:
-  `dstip`     - Dstip (ipv4|ipv6)
-  `dstip1`    - Dstip1 - octet one (ipv4|ipv6)
-  `dstip2`    - Dstip2 - octet two (ipv4|ipv6)
-  `dstip3`    - Dstip3 - octet three (ipv4|ipv6)
-  `dstip4`    - Dstip4 - octet four (ipv4|ipv6)
-  `dstport`   - Dstport
-  `dstport1`  - Dstport1 - octet one
-  `dstport2`  - Dstport2 - octet two
-  `ipflags`   - IP flags
-  `proto`     - Protocol
-  `srcip`     - Srcip (ipv4|ipv6)
-  `srcip1`    - Srcip1 - octet one (ipv4|ipv6)
-  `srcip2`    - Srcip2 - octet two (ipv4|ipv6)
-  `srcip3`    - Srcip3 - octet three (ipv4|ipv6)
-  `srcip4`    - Srcip4 - octet four (ipv4|ipv6)
-  `srcport`   - Srcport
-  `srcport1`  - Srcport1 - octet one
-  `srcport2`  - Srcport2 - octet two
-  `tcpflags`  - TCP flags
-  `tcpflags1` - TCP flags 1 - octet one
-  `tcpflags2` - TCP flags 2 - octet two


##### Syntax

`eval-items <string>`

---

#### required-items

Specifies required items which must be a part of the final filter. If the filter is missing some of the required items, it is discarded and not used in the mitigation phase. More than one `required-items` can be configured, then one of them must be fulfilled.

List of available items:
-  `dstip`     - Dstip (ipv4|ipv6)
-  `dstip1`    - Dstip1 - octet one (ipv4|ipv6)
-  `dstip2`    - Dstip2 - octet two (ipv4|ipv6)
-  `dstip3`    - Dstip3 - octet three (ipv4|ipv6)
-  `dstip4`    - Dstip4 - octet four (ipv4|ipv6)
-  `dstport`   - Dstport
-  `dstport1`  - Dstport1 - octet one
-  `dstport2`  - Dstport2 - octet two
-  `ipflags`   - IP flags
-  `proto`     - Protocol
-  `srcip`     - Srcip (ipv4|ipv6)
-  `srcip1`    - Srcip1 - octet one (ipv4|ipv6)
-  `srcip2`    - Srcip2 - octet two (ipv4|ipv6)
-  `srcip3`    - Srcip3 - octet three (ipv4|ipv6)
-  `srcip4`    - Srcip4 - octet four (ipv4|ipv6)
-  `srcport`   - Srcport
-  `srcport1`  - Srcport1 - octet one
-  `srcport2`  - Srcport2 - octet two
-  `tcpflags`  - TCP flags
-  `tcpflags1` - TCP flags 1 - octet one
-  `tcpflags2` - TCP flags 2 - octet two

##### Syntax

`required-items <string>`

---

#### reset-baseline

Resets baseline computations (starts to compute baseline from the current traffic).

##### Syntax

`reset-baseline`

---

#### clear-filters

Clears all active filters.

##### Syntax

`clear-filters`


## Configuring Template

### Context

`template` command has own subcontext. It is possible to switch to the subcontext using the following command.

```
netx# ddos-guard template <template-name>
netx(ddg-template-templatename)#
```

---

#### threshold

See [threshold](ddos-guard.md#threshold) in rule configuration section.

---

#### filter-timeout

See [filter-timeout](ddos-guard.md#filter-timeout) in rule configuration section.

---

#### baseline-coefficient

See [baseline-coefficient](ddos-guard.md#baseline-coefficient) in rule configuration section.

---

#### pass-action

See [pass-action](ddos-guard.md#pass-action) in rule configuration section.

---

#### filter-action

See [filter-action](ddos-guard.md#filter-action) in rule configuration section.

---

#### eval-step-msecs

See [eval-step-msecs](ddos-guard.md#eval-step-msecs) in rule configuration section.

---

#### report-mail

See [report-mail](ddos-guard.md#report-mail) in rule configuration section.

---

#### report-bgp-flowspec

See [report-bgp-flowspec](ddos-guard.md#report-bgp-flowspec) in rule configuration section.

---

#### description

See [description](ddos-guard.md#description) in rule configuration section.

---

#### eval-items

See [eval-items](ddos-guard.md#eval-items) in rule configuration section.

---

#### required-items

See [required-items](ddos-guard.md#required-items) in rule configuration section.

---

## Configuration example

This example shows protection against attacks on udp port 123 (ntp).

1. Firewall configuration - sending traffic on port 123 to DDoS Guard. ddg-rule identifies the DDoS Guard rule and should be used also as rule identification in the ddos-guard rule context.

```
table raw chain PREROUTING
	action DDG id 1 in hge11
table raw chain DDG
	action DDOSGUARD id 1 proto udp sport 123 ddg-rule 010ntp
```

2. DDoS Guard basic template configuration - Creating a defconf template with mail report configuration. Setting filter to drop packets.

```
netx# ddos-guard template defconf
netx(ddg-template-defconf)# report-mail example@netx.as
netx(ddg-template-defconf)# filter-action DROP
```

3. Setting `rule` basic configuration.

```
netx# ddos-guard rule 010ntp
netx(ddg-010ntp)# template defconf
netx(ddg-010ntp)# threshold bps 100M pps-baseline-derived 3 pps 20k bps-baseline-derived 3
netx(ddg-010ntp)# eval-items proto srcip dstip srcport dstport
netx(ddg-010ntp)# required-items dstip dstport
```

4. Enabling DDoS Guard

```
netx# ddos-guard enable
```

5. Verifying configuration

```
netx# monitor ddos-guard rule 010ntp
```

Live configuration output with all the important parameters:

```
CONFIG:
Rule:		010ntp
Filter timeout:	60s
Eval-step time:	1000ms
Eval items:	family proto srcip dstip srcport dstport
Required items:	dstip dstport
Filter action:	DROP
Passed action:	CONTINUE
----------------------------------------------------------------------
COUNTERS:	   p/s       b/s
Baseline:  	  19.6k     73.0M (baseline-coefficient: 300)
Threshold: 	  20.0k    100.0M (baseline-derived multiplier: 3/3, min. 0/0, max. 20.0k/100.0M)
Limit:     	  20.0k    100.0M
Total:     	  53.3k    199.0M
Blocked:   	   0.0       0.0
Passed:    	  32.0k    119.9M
----------------------------------------------------------------------
TRAFFIC INSPECTION: ANALYZING  (15.0k p/s 75.0M b/s, step: 3)
Protocol:	 ......
Addr:		 ............:..... -> ............:.....
Flags:		 .....
----------------------------------------------------------------------
FILTERS:
PROTO  SRC                   DST                   REM    p/s     b/s
```
