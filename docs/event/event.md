# Event manager

An event manager is a tool that is used to manage events and automate certain tasks to run at specific times. Event manager provides a way to react to a range of events. When event occurs, the defined action is started.

Watching interface state changes, changes in routing and rest api endpoints monitoring are supported.

Actions are defined as script name. More than one action can be defined in the event. Event parameters are sent to script as arguments.

### Context

It is possible to switch to the Event manager context using `event` command.

```
netx# event <event name>
netx(event)# <command>
```

### Commands

The following commands are available in event context.

#### watch

Watching changes in routing tables, interfaces state changes and rest api endpoint monitoring are supported.

Event manager routes monitoring supports `exact-match` or `subnet` parameters. Parameter  `exact-match` causes matching only the exact route in the routing table (by default `exact-match` parameter is used). Parameter `subnet` causes also subnetworks matching.

Event manager can monitor any interface configured in NetX.

Rest api endpoint supports sending additional data as url parameters. These parameters are sent to action script as arguments.

##### Syntax

`watch <route|interface|rest>`
`watch route [subnet|exact-match] [table <routing table number>]`
`watch interface <interface name>`
`watch rest <rest endpoint>`

##### Examples

```
watch interface tge1
watch route 192.168.0.0/16 subnet table 10
watch rest restendpoint
```

---

#### action

Path to script which is started after the event occurs. Event parameters are sent to script as arguments. More than one action can be defined per event. In case of interface/route monitoring, `up` or `down` optional parameter can be configured to run only when new route is added/deleted or interface changed state to up/down.

##### Syntax

`action <script> [up|down]`

---


## Display configuration

It's possible to use `show event [event name]` command to display information about event manager.

```
Event name          : event
Action              : /etc/netc/events/actionscript
Route               : 192.168.1.0/24 table 10
Rest endpoint       : restendpoint
Last matched        : <never>
```
