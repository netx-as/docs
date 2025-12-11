# PPPoE Server

The NetX platform includes a built-in PPPoE (Point-to-Point Protocol over Ethernet) server, allowing it to act as a broadband remote access server (BRAS). This is useful for providing internet access to clients over Ethernet networks, authenticating them, and managing their sessions.

## Configuration Context

All PPPoE server configuration is done within the `pppoe-server` context.

```
netx# pppoe-server
netx(pppoe)# 
```

## Basic Configuration

To set up a basic PPPoE server, you need to define the interfaces where the server will listen, configure authentication secrets, and enable the service.

### 1. Managing Interfaces

You must specify which network interfaces the PPPoE server should listen on.

**Add an interface:**
```
netx(pppoe)# interfaces add <interface_name>
```
Example:
```
netx(pppoe)# interfaces add eth1.100
```

**Delete an interface:**
```
netx(pppoe)# interfaces delete <interface_name>
```

**Show configured interfaces:**
```
netx(pppoe)# interfaces
```

### 2. Configuration and Secrets

The PPPoE server uses standard configuration files for options and user secrets (CHAP/PAP).

**Main Configuration File:**
You can specify a custom configuration file, or use the default.
```
netx(pppoe)# config-file /etc/ppp/pppoe-server-options
```

To edit the configuration file directly from the CLI:
```
netx(pppoe)# edit-config
```

**Secrets File:**
This file contains the usernames and passwords for client authentication.
```
netx(pppoe)# secrets-file /etc/ppp/chap-secrets
```

To edit the secrets file directly from the CLI:
```
netx(pppoe)# edit-secrets
```

### 3. Enabling the Server

Once configured, enable the PPPoE server:

```
netx(pppoe)# enable
```

To disable it:
```
netx(pppoe)# no enable
```

## Session Management

You can monitor and manage active PPPoE sessions directly from the CLI.

**Show all active sessions:**
```
netx(pppoe)# show pppoe-server sessions
```

**Show session details by IP:**
```
netx(pppoe)# show pppoe-server sessions ip <ip_address>
```

**Show session details by Username:**
```
netx(pppoe)# show pppoe-server sessions user <username>
```

**Terminate a session:**
To disconnect a user, you can use the `no` command (which maps to `terminate_session` internally) or specific commands if available. Based on the CLI structure:

```
netx(pppoe)# no sessions ip <ip_address>
netx(pppoe)# no sessions user <username>
```

## Example Configuration

```
netx# pppoe-server
netx(pppoe)# interfaces add eth2
netx(pppoe)# config-file /etc/ppp/pppoe.cfg
netx(pppoe)# secrets-file /etc/ppp/chap-secrets
netx(pppoe)# edit-secrets
# Add user: "user1" * "password" *
netx(pppoe)# enable
```
