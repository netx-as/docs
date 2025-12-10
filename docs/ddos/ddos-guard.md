# DDoS Guard

DDoS Guard is a built-in NetX component for DDoS attack detection and mitigation. The core of the DDoS Guard is implemented as an iptables kernel module. It consists of two parts: detection and mitigation (called filtration).

The detection phase counts the number of packets per second (pps) and bytes per second (bps) passing through the system. It computes baselines from actual traffic and sets a threshold. If the threshold is exceeded, the algorithm begins evaluating the configured items (e.g., source port, destination IP address, etc.). These items are evaluated, and a final filtration rule is created. Several parameters affect the detection phase, which are detailed in the following sections.

The mitigation phase starts after the filtration rule is created. Several actions can be taken. DDoS Guard can apply this filtration rule and filter packets internally before they hit the system. Another option is to use BGP Flowspec to propagate filtering rules into the network to mitigate the effects of a DDoS attack. Each filtration rule has a timeout, which starts after the traffic drops below the threshold.

Configuration is performed in two places. First, the firewall rule must be configured (action `DDOSGUARD`) to define which traffic is forwarded to the DDoS Guard. Second, the `ddos-guard` context provides additional configuration. The example section below explains this with concrete examples.

### Context

Switch to the DDoS Guard context using the `ddos-guard` command.

```
netx# ddos-guard
netx(ddg)# <command>
```

### Commands

The following commands are available in the `ddos-guard` context.

#### enable

Enable the DDoS Guard engine.

##### Syntax

`enable`

##### Default value

DDoS Guard is disabled by default.

---

#### log-level

Logging level severity option. You can choose between `info` and `debug` log severity.

##### Syntax

`log-level <info | debug>`

##### Default value

If `log-level` is not provided, `info` is the default value.

---

## Configuring BGP Flowspec Reporting

Basic BGP configuration is used for filter reporting via BGP Flowspec.
Switch to the BGP context using the `bgp` command.

### Context

The `bgp` command has its own subcontext. Switch to the subcontext using the following command:

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

The `rule` command has its own subcontext. Switch to the subcontext using the following command:

```
netx# ddos-guard rule <rule-name>
netx(ddg-rulename)#
```

---

#### template

DDoS Guard template configuration. A rule inherits configuration from a template. If configuration settings conflict, the rule configuration takes precedence over the template configuration.

##### Syntax

`template <string>`

---

#### threshold

As described above, the threshold is a crucial parameter that starts the detection process. There are several ways to configure the threshold:

1.  **Based on baseline**: The recommended way is to compute the threshold automatically based on the baseline. The baseline represents average traffic computed from history. The baseline is then multiplied by a coefficient called `baseline-derived` to calculate the threshold. `baseline-derived` is 3 by default (can be changed), which means that traffic must be three times higher than the average to start the detection phase.
2.  **Manually configured thresholds**: Thresholds can also be configured manually. This is not recommended unless you have a precise understanding of the affected network and traffic. The recommended way to use a manual threshold is to combine it with configuration based on the baseline. In this case, the configured threshold acts as the maximal threshold. This means that when this threshold is exceeded, detection starts regardless of the baseline-based threshold. For example, this can be used as a last resort protection before the link is saturated or systems are overloaded.
3.  **Manually configured minimal thresholds**: This parameter can be configured in combination with baseline-based threshold configuration. It means that the threshold computed by the baseline must be at least the minimal threshold.

Threshold configuration contains several options for detailed settings.

##### Syntax

`threshold <opts>`

---

### Threshold options

#### threshold pps

Threshold packets per second. In case of an active baseline-based threshold calculation, `pps` is used as the maximal packet threshold.

##### Syntax

`pps <num>[<.num>]<suffix>`


##### Example

`pps 20k`

---

#### threshold bps

Threshold bytes per second. In case of an active baseline-based threshold calculation, `bps` is used as the maximal bytes threshold.

##### Syntax

`bps <num>[<.num>]<suffix>`


##### Example

`bps 100M`

---

#### threshold pps-min

Threshold minimal packets per second. In case of an active baseline-based threshold calculation, `pps-min` is used as a minimal packet threshold.

##### Syntax

`pps-min <num>[<.num>]<suffix>`


##### Example

`pps-min 5k`

---

#### threshold bps-min

Threshold minimal bytes per second. In case of an active baseline-based threshold calculation, `bps-min` is used as a minimal bytes threshold.

##### Syntax

`bps-min <num>[<.num>]<suffix>`


##### Example

`bps-min 25M`

---

#### threshold pps-baseline-derived

A coefficient by which the baseline is multiplied to get the current threshold. Configuring this parameter enables baseline-based threshold computation for packets per second.

##### Syntax

`pps-baseline-derived <num>`


##### Example

`pps-baseline-derived 3`

---

#### threshold bps-baseline-derived

A coefficient by which the baseline is multiplied to get the current threshold. Configuring this parameter enables baseline-based threshold computation for bytes per second.

##### Syntax

`bps-baseline-derived <num>`


##### Example

`bps-baseline-derived 5`

---

#### limit

Limits the traffic rate during mitigation (policing). This acts as a hard cap on traffic when the threshold is exceeded.

##### Syntax

`limit <opts>`

**Options:**
*   `pps <value>`: Limit packets per second.
*   `bps <value>`: Limit bytes per second.

##### Example

`limit pps 50k`

---

#### filter-timeout

The timeout in seconds after which the filtering rule is removed. This timeout starts only when the filtering traffic drops below the threshold.

##### Syntax

`filter-timeout <number>`

##### Default value

The default filter timeout is 60 seconds.

---

#### baseline-coefficient

The baseline coefficient represents the time range from which the baseline is computed.

##### Syntax

`baseline-coefficient <number>`

##### Default value

The default baseline coefficient is 300 seconds (last 5 minutes).

---

#### pass-action

The action applied to packets not matched by any filter. These are the packets matched by the firewall rule and analyzed by DDoS Guard but not matching any specific attack pattern.

##### Syntax

`pass-action <CONTINUE>|<ACCEPT>|<RETURN>|<DROP>`

##### Default value

The default `pass-action` is `CONTINUE`.

---

#### filter-action

The action applied to packets matched by a found filter (attack traffic).

##### Syntax

`filter-action <CONTINUE>|<ACCEPT>|<RETURN>|<DROP>`

##### Default value

The default `filter-action` is `CONTINUE`.

---

#### eval-step-msecs

The evaluation time between algorithm steps (time between checking the traffic against the threshold or matching the next evaluation item). Evaluation time is configured in milliseconds.

##### Syntax

`eval-step-msecs <number>`

##### Default value

The default evaluation time is 1000 milliseconds (1 second).

---

#### report-mail

Email address used for reporting. More than one email address can be configured. Report alerts are sent at the start and end of a DDoS attack.

##### Syntax

`report-mail <string>`

---

#### report-bgp-flowspec

Enables reporting via BGP Flowspec.

##### Syntax

`report-bgp-flowspec`

---

#### description

Rule description.

##### Syntax

`description <string>`

---

#### eval-items

Items to be searched when detecting a DDoS attack. Items are searched in the specified order.

List of available items:
-  `dstip`     - Destination IP (IPv4|IPv6)
-  `dstip1`    - Destination IP - octet one
-  `dstip2`    - Destination IP - octet two
-  `dstip3`    - Destination IP - octet three
-  `dstip4`    - Destination IP - octet four
-  `dstport`   - Destination Port
-  `dstport1`  - Destination Port - octet one
-  `dstport2`  - Destination Port - octet two
-  `ipflags`   - IP flags
-  `proto`     - Protocol
-  `srcip`     - Source IP (IPv4|IPv6)
-  `srcip1`    - Source IP - octet one
-  `srcip2`    - Source IP - octet two
-  `srcip3`    - Source IP - octet three
-  `srcip4`    - Source IP - octet four
-  `srcport`   - Source Port
-  `srcport1`  - Source Port - octet one
-  `srcport2`  - Source Port - octet two
-  `tcpflags`  - TCP flags
-  `tcpflags1` - TCP flags 1 - octet one
-  `tcpflags2` - TCP flags 2 - octet two


##### Syntax

`eval-items <string>`

---

#### required-items

Specifies the items that must be part of the final filter. If the filter is missing any of the required items, it is discarded and not used in the mitigation phase. If multiple `required-items` are configured, at least one of them must be fulfilled.

List of available items:
-  `dstip`     - Destination IP (IPv4|IPv6)
-  `dstip1`    - Destination IP - octet one
-  `dstip2`    - Destination IP - octet two
-  `dstip3`    - Destination IP - octet three
-  `dstip4`    - Destination IP - octet four
-  `dstport`   - Destination Port
-  `dstport1`  - Destination Port - octet one
-  `dstport2`  - Destination Port - octet two
-  `ipflags`   - IP flags
-  `proto`     - Protocol
-  `srcip`     - Source IP (IPv4|IPv6)
-  `srcip1`    - Source IP - octet one
-  `srcip2`    - Source IP - octet two
-  `srcip3`    - Source IP - octet three
-  `srcip4`    - Source IP - octet four
-  `srcport`   - Source Port
-  `srcport1`  - Source Port - octet one
-  `srcport2`  - Source Port - octet two
-  `tcpflags`  - TCP flags
-  `tcpflags1` - TCP flags 1 - octet one
-  `tcpflags2` - TCP flags 2 - octet two

##### Syntax

`required-items <string>`

---

#### reset-baseline

Resets baseline computations (starts computing the baseline from current traffic).

##### Syntax

`reset-baseline`

---

#### clear-filters

Clears all active filters.

##### Syntax

`clear-filters`


## Configuring Template

### Context

The `template` command has its own subcontext. Switch to the subcontext using the following command:

```
netx# ddos-guard template <template-name>
netx(ddg-template-templatename)#
```

---

#### threshold

See [threshold](#threshold) in the rule configuration section.

---

#### limit

See [limit](#limit) in the rule configuration section.

---

#### filter-timeout

See [filter-timeout](#filter-timeout) in the rule configuration section.

---

#### baseline-coefficient

See [baseline-coefficient](#baseline-coefficient) in the rule configuration section.

---

#### pass-action

See [pass-action](#pass-action) in the rule configuration section.

---

#### filter-action

See [filter-action](#filter-action) in the rule configuration section.

---

#### eval-step-msecs

See [eval-step-msecs](#eval-step-msecs) in the rule configuration section.

---

#### report-mail

See [report-mail](#report-mail) in the rule configuration section.

---

#### report-bgp-flowspec

See [report-bgp-flowspec](#report-bgp-flowspec) in the rule configuration section.

---

#### description

See [description](#description) in the rule configuration section.

---

#### eval-items

See [eval-items](#eval-items) in the rule configuration section.

---

#### required-items

See [required-items](#required-items) in the rule configuration section.

---

## Configuration example

This example demonstrates protection against attacks on UDP port 123 (NTP).

1.  **Firewall configuration**: Send traffic on port 123 to DDoS Guard. The `ddg-rule` parameter identifies the DDoS Guard rule and must match the rule name in the `ddos-guard` context.

```
netx# ipv4 firewall
netx(fw4)# table raw chain PREROUTING
netx(fw4-raw-PREROUTING)# action DDG

netx# ipv4 firewall
netx(fw4)# table raw chain DDG
netx(fw4-raw-DDG)# action DDOSGUARD id 1 proto udp sport 123 ddg-rule 010ntp
```

2.  **DDoS Guard basic template configuration**: Create a `defconf` template with mail report configuration and set the filter action to DROP.

```
netx# ddos-guard template defconf
netx(ddg-template-defconf)# report-mail example@netx.as
netx(ddg-template-defconf)# filter-action DROP
```

3.  **Setting basic rule configuration**:

```
netx# ddos-guard rule 010ntp
netx(ddg-010ntp)# template defconf
netx(ddg-010ntp)# threshold bps 100M pps-baseline-derived 3 pps 20k bps-baseline-derived 3
netx(ddg-010ntp)# eval-items proto srcip dstip srcport dstport
netx(ddg-010ntp)# required-items dstip dstport
```

4.  **Enabling DDoS Guard**:

```
netx# ddos-guard enable
```

5.  **Verifying configuration**:

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
