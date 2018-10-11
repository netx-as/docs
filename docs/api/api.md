# REST API

> [!TIP]
> Check also the folowing tutorials:
> * [Set up firewall via REST API](~/tutorials/api/firewall.md)
> * [Blacklist for a temporary block of IP addresses](~/tutorials/api/blacklist.md)
> * [Token based authentication](~/tutorials/api/token.md)

NETX routers can be configured either via `netc` CLI shell or via REST API. REST API allows to integrate and automate
the whole configuration process with your internal system or via any HTTP client. All commands available in CLI are available via
REST API as well. REST API returns `JSON` objects for further processing and parsing. API is available via the following URL:

```
http[s]://<netx-address>/api/
```

The access to the API is protected via standard HTTP Authentication (HTTP Authorization header) or via [JSON Web Tokens](https://jwt.io). 
HTTP Authentication uses the same username and password as for SSH access - see [Default configuration](~/docs/default-config.md) for default 
username/password or [Login Credentials](~/docs/system/basics.md#user-management) for user management. REST API uses the following three methods 
for data manipulation.

* **GET**		List an entry, obtain an entry details
* **POST**    	Create a new entry, modify an entry
* **DELETE**  	Delete an entry

## Simple example
The following commands are very simple examples of REST API usage for those impatient. There is `rest-netc-client` demo client
available for basic testing. It is, however, possible to use `cURL` or other HTTP client according the needs. 

* Creating a loopback interface `lo2`

The following command is equivalent to `netx# interface lo2` and creates loopback interface `lo2`. `JSON` object is received
in response with a status code and message.

```
# curl -X POST -u user:password https://<netx-address>/api/interface/lo2

{
  "Request": {
    "PostData": {},
    "Node": [
      "interface",
      "lo2"
    ]
  },
  "Message": [
    "Creating loopback interface lo2",
    "\n"
  ],
  "RequestStatus": "OK"
}
```

* Deleting loopback interface `lo2`

The command `netx# no interface lo2` is the same as the following API call. The method is `DELETE`, otherwise the command is the same.

```
# curl -X DELETE -u user:password https://<netx-address>/api/interface/lo2

{
  "Request": {
    "PostData": {},
    "Node": [
      "interface",
      "lo2"
    ]
  },
  "Message": [
    "Removing loopback interface lo2",
    "\n"
  ],
  "RequestStatus": "OK"
}
```

## URL format 
The URL format is the same as calling the command directly in `netc` shell. The URL is encoded according to [RFC 3986](https://tools.ietf.org/html/rfc3986). 
If used in a script or automation tool, it is necessary to ensure that Reserved Characters (e.g., `/`, `*`) are properly encoded if they are part of 
the command. For example, the following command must be properly encoded using Percent-Encoding as the `/` is a part of the URL path.

```
GET https://<netx-address>/api/interface/tge1/ipv4/address/100.100.100.84%2F24
```

It is possible to add other parameters to URL by setting a query. Options `debug` and `output` are supported.

| Query   | Supported values | Meaning |
| ---     | ---              | ---     |
| debug=value    |   0 or 1   |               Enable or disable debug information |
|output=format  |   `json` or `dumper` |     Answer is returned according the format. If `json` is set, `JSON` object is returned. If `dumper` is set, internal perl structures are printed |


## Return value

The HTTP return values and status codes conform with [RFC 2616](https://tools.ietf.org/html/rfc3986). 

|Code |      Description |
| --- |    ------------------------------------------------------ |
| 200  |      The request has succeeded. The information returned with the response is dependent on the method used in the request and is sent in structured `JSON` format by default. |
| 400  |      The request could not be understood by the NETX router.  The error details are sent using structured `JSON` format. The client should be able to handle the error and should not repeat the request without a modification. |
| 401 |       Unauthorized access. |
| Other |      Other codes are returned according to RFC 2616 convention. |

## GET Method

The GET Method returns information about the requested node together with information about
subnodes (if available). Metadata information about the nodes are returned as well so it is possible
to use them in following POST/DELETE methods.

### Highest level attributes

| Attribute |        Type |                   Description |
| --- |---|---| 
| NodeRequest |      @array  |                API Request split to nodes |
| RequestStatus |    `OK`, `Error` |          Result of the request |
| ErrorStatus  |     string   |               Error string if request could not be completed.    |
|NodeInfo          | structure |              The structure describing node's properties.|

### NodeInfo structure attributes

Attribute         | Type |                    Description
---| ---| ---|
Name |             string                  | Node name
Type  |            `Token`, `Value`  |      The node can be of two types. `Token` type is the pernament node name (e.g., interface). `Value` is a node that can have different names (e.g., name of the interface 'tge1'). If Type is set to `Value`, it can have one or several values (depends on `MultiValue` flag).
AllowSet  |        `0` or `1`  |            If set to `1`, `SET` operation is allowed for the node.  E.g., node `interface tge1 ip address` has `AllowSet` set to `0` as the node is not complete. However, node `interface tge1 ip address 1.1.1.1/24` is complete, thus `AllowSet` is set to `1`
AllowUnset       | `0` or `1` |             Similar as AllowSet but for `UNSET`/`DELETE` operation.
AllowShow       |  `0` or `1` |             Same as above for `SHOW` operation.
HasSetSubnodes   | `0` or `1` |             Set to `1` if the node has other subnodes available for `SET` operation.
HasUnSetSubnodes | `0` or `1` |             Set to `1` if the node has other subnodes available for `UNSET` operation.
HasShowSubnodes  | `0` or `1` |             Set to `1` if the node has other subnodes available for `SHOW` operation.
HasSubnodes     |  `0` or `1` |             Set to `1` if the node has other subnodes available.
SetValues       |  `@array`   |             If node type is `Value` (see above), it contains array of currently set (configured) values for the node.
SetOptions      |  `@array of %hashes` |    Array of hashes. Every key in the hash contains array of configured values. The position in `@array` correspond with position in `SetValues` array.
PossibleValues   |  `@array`         |      Possible values that can be set for the node. It's a hint. A different value matches the `InputRe` can be set as well. 
PossibleOptions  |  `%hash` array     |     Hash array of possible options. See `OptionInfo` for details.  
MultiValue      |  `0` or `1`         |     If the node type is Value (see above) and MultiValue is set to `1`, the node can have several different values. 
SubNodes        |  `@array`           |     An array containing `NodeInfo` sructure for subnodes.  
Description     |   string            |     Description of the node. Optional.
Help            |   string            |     Help text for the node type Value. E.g. for `ipv4 address` the help text is `<x.x.x.x/x>`, for string `<str>`, for number `<num>`, etc.  
InputRe         |   string            |     Regular expression for node type `Value`. The value set for the node must match the regexp.
ShowOutput      |   string/table      |     The output of show command for the node. Included only if `show` parameter in POST method is set. The output is text or table, depends on ShowFormat value (see below).  
ShowFormat      |   `text`, `table`   |     Set the output format for ShowOutput.
PossibleOptions  |   structure        |      Different options for the node. See OptionInfo.

The following example shows output of `/api/interface` command. 

```
# curl -X GET -u user:passwd https://<netx-address>/api/interface | jq '.'

{
  "NodeInfo": {
    "HasSubnodes": 1,
    "Description": "network interfaces",
    "Name": "interface",
    "AllowSet": 0,
    "AllowShow": 1,
    "Type": "Token",
    "HasShowSubnodes": 1,
    "SubNodes": [
      {
        "Help": "<ifname.vlanid>",
        "MultiValue": 0,
        "HasSubnodes": 1,
        "Description": "interface name",
        "Name": "%IF",
        "HasUnSetSubnodes": 1,
        "AllowUnSet": 1,
        "InputRe": "([\\w\\-\\.\\d]+)",
        "SetValues": [
          "lo1",
          "bond0",
          "ve1",
          "ve2",
          "ve3",
          "ve4",
          "ve2.110",
          "ve2.113",
          "ve2.114",
          "ve3.115",
          "ve2.1710"
        ],
        "AllowSet": 1,
        "AllowShow": 1,
        "Type": "Value",
        "HasShowSubnodes": 1,
        "PossibleValues": [
          "lo1",
          "bond0",
          "ve1",
          "ve2",
          "ve3",
          "ve4",
          "ve2.110",
          "ve2.113",
          "ve2.114",
          "ve3.115",
          "ve2.1710"
        ],
        "HasSetSubnodes": 1
      }
    ],
    "AllowUnSet": 0,
    "HasSetSubnodes": 1,
    "HasUnSetSubnodes": 1
  },
  "Request": {
    "Node": [
      "interface"
    ]
  },
  "RequestStatus": "OK"
}
```

### OptionInfo structure attributes

Attribute        | Type                |    Description
--------------   | ------------------  |    --------------------------------------------------------
InputRe          | string              |    Regular expression that must match the option value. 
ValueType        | string              |    Available only for non-binary value. E.g. `%NUM` for number.
Count            | number              |    How many times can the option be repeated.
Description      | string              |    Description of the option.
AvailableInSet   | `0` or `1`          |    The option can be used for Set/POST method.
AvailableInUnSet | `0` or `1`          |    The option can be used for UnSet/DELETE method.
AvailableInShow  | `0` or `1`          |    The option can be used for showing other info.
Key              | `0` or `1`          |    If set, the option is the key for SetValues and SetOption combination. In that case, it must be used for UnSet/DELETE method.

Example of the OptionInfo structure can be seen by calling `ping` command.

```
# curl -X GET -u user:passwd https://<netx-address>/api/ping | jq '.'
{
  "NodeInfo": {
    "HasSubnodes": 1,
    "Description": "ping commnad",
    "Name": "ping",
    "HasUnSetSubnodes": 0,
    "AllowSet": 0,
    "AllowShow": 0,
    "Type": "Token",
    "PossibleOptions": {
      "size": {
        "Description": "packet size in Bytes",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "ValueType": "%NUM",
        "Count": 1,
        "AvailableInUnSet": 0,
        "InputRe": "(\\d+)"
      },
      "interval": {
        "Description": "set wait interval in seconds",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "ValueType": "%NUM",
        "Count": 1,
        "AvailableInUnSet": 0,
        "InputRe": "(\\d+)"
      },
      "numeric": {
        "Description": "do not lookup DNS names",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "Count": 1,
        "AvailableInUnSet": 0
      },
      "interface": {
        "Description": "output interface name",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "ValueType": "%IF",
        "Count": 1,
        "AvailableInUnSet": 0,
        "InputRe": "([\\w\\-\\.\\d]+)"
      },
      "count": {
        "Description": "number of packets",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "ValueType": "%NUM",
        "Count": 1,
        "AvailableInUnSet": 0,
        "InputRe": "(\\d+)"
      },
      "source": {
        "Description": "source ip address",
        "AvailableInSet": 1,
        "AvailableInShow": 0,
        "ValueType": "%IP4",
        "Count": 1,
        "AvailableInUnSet": 0,
        "InputRe": "([\\d\\.\\/]+)"
      }
    },
    "HasShowSubnodes": 0,
    "SubNodes": [
      {
        "Help": "<x.x.x.x>",
        "MultiValue": 0,
        "HasSubnodes": 0,
        "Description": "IPv4 address",
        "Name": "%IP4",
        "HasUnSetSubnodes": 0,
        "AllowUnSet": 0,
        "InputRe": "([\\d\\.\\/]+)",
        "SetValues": null,
        "AllowSet": 1,
        "AllowShow": 0,
        "Type": "Value",
        "HasShowSubnodes": 0,
        "PossibleValues": null,
        "HasSetSubnodes": 0
      }
    ],
    "HasSetSubnodes": 1,
    "AllowUnSet": 0
  },
  "Request": {
    "Node": [
      "ping"
    ]
  },
  "RequestStatus": "OK"
}
```

## POST Method 

This method is used for configuration of new values or modification existing nodes. The method can be
used either directly without a parameter or pass an Option structure. Return code follows RFC 2616 convention.
A `Message` attribute with the description can be included in the output if necessary. E.g.

```
POST interface/tge1.112 

{ 
  "RequestStatus":"OK",
  "Message": [ "Creating vlan interface tge1.226" ]
}
```

POST method can be used also as a substitution to GET or DELETE methods. This behavior is controlled by `Action` attribute -- see below.
 
### Input attributes

Attribute    |     Type               |     Description
--------------|    ------------------ |     --------------------------------------------------------
Actions       |    `@array`           |     Array of actions that should be run. By default it contains only `SET` action. Possible values: `SET`, `UNSET`, `GET`, `SHOW`.  E.g. If the attribute is set to `[ 'SET', 'GET' ]`, `SET` method will be run together with the `GET` method to obtain the result.
Options        |   `%hash` array      |     Additional options that can be passed. The values that can be used are described in `OptionInfo` structure in `GET` method.

### Return attributes

Attribute      |   Type                |    Description
-------------- |   ------------------  |    --------------------------------------------------------
NodeRequest    |   `@array`            |    Request splitted to single nodes.
RequestStatus  |   `OK`, `ERROR`       |    The status of the request.
ErrorStatus    |   string              |    Error message
Message        |   string              |    Output of the request. Optional.

## DELETE Method 

This method is used for deleting particular node. Return code follows RFC 2616 convention.
A `Message` attribute with the description can be included in the output if necessary. E.g.,

```
DELETE interface/tge1.112 

{ 
  "RequestStatus":"OK",
  "Message": [ "Removing vlan interface tge2.111" ]
}
```

### Return attributes

Attribute      |   Type                |    Description
-------------- |   ------------------  |    --------------------------------------------------------
NodeRequest    |   `@array`            |    Request splitted to single nodes.
RequestStatus  |   `OK`, `ERROR`       |    The status of the request.
ErrorStatus    |   string              |    Error message
Message        |   string              |    Output of the request. Optional.

 
## Demo client 

It is possible to use any compatible HTTP client for calling the API method, e.g. curl. If curl is not an
option, it is possible to use a demo client (`rest-netc-client`) for basic testing or as a template for
custom API application.

### Available options

Option         |   Description
-------------- |   ------------------      
`-p`           |   Use `POST` method insted of default `GET` method
`-d`           |   Use `DELETE` method insted of default `GET` method
`-s`           |   Set server's IP address. Default value: `localhost`
`-A <action>`  |   Available for `POST` method only. Several methods can be set (e.g. -A SET,GET). See Action attribute in POST method.
`-O <options>` |   Set Option attribute in POST method. Syntax is key=value, e.g. `-O src=1.1.1.1/24`
`-n`           |   How many times should be the command repeated. Useful for testing the response time. 
