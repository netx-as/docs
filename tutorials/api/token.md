# Token API access

NETX routers offer REST API that allows to integrate and automate the whole configuration process with your internal system.
All commands available in CLI are available via REST API as well. REST API returns `JSON` objects for further processing and 
parsing. The access to the API is protected via standard HTTP Authentication (HTTP Authorization header) or via 
[JSON Web Tokens](https://jwt.io). It's also possible to give access to the API only to a selected user. The following tutorial 
shows how to use the token based authentication.

1. Let's create a user (`api-user`) that will be used only for token based authentication. We will not set a password for 
the user, thus, the user will be denied to log in via SSH or console and cannot be compromised.

```
netx# system user api-user

! we can verify, that the user is created
netx# show system user
admin
api-user
```

2. To obtain the token, `create-token` command is used in `user api` context. 

```
netx# system user api-user api create-token 
eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE1MzkxODkyNjgsImlhdCI6MTUzOTE4NzQ2OCwibmJmIjoxNTM5MTg3NDY4LCJ1c2VyIjoiYXBpLXVzZXIifQ.P7fmdvJvb6b_VSLOYEYW3R7D4VuCRybYyuzPF0sbv_ot2fQ_efJ6ey9F1VUhUKvlP4ls661CEsr5g1vBwkOA_w

! Hurray! We received our token
```

3. The token can be used in REST API request. It's necessary to set Authorization header appropriately to `Authorization: Bearer`.

> [!NOTE]
> The URL for token API access is api-oauth!

```
curl -k https://<netx-address>/api-oauth/interface -H "Authorization: Bearer eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE1MzkxODkyNjgsImlhdCI6MTUzOTE4NzQ2OCwibmJmIjoxNTM5MTg3NDY4LCJ1c2VyIjoiYXBpLXVzZXIifQ.P7fmdvJvb6b_VSLOYEYW3R7D4VuCRybYyuzPF0sbv_ot2fQ_efJ6ey9F1VUhUKvlP4ls661CEsr5g1vBwkOA_w" | jq '.' 

{
  "RequestStatus": "OK",
  "Request": {
    "Node": [
      "interface"
    ]
  },
  "NodeInfo": {
    "AllowSet": 0,
    "AllowShow": 1,
    "Type": "Token",
    "HasShowSubnodes": 1,
    "SubNodes": [
      {
        "InputRe": "([\\w\\-\\.\\d]+)",
        "SetValues": [
          "ve1",
          "ve2"
        ],
        "AllowSet": 1,
        "AllowShow": 1,
        "Type": "Value",
        "HasShowSubnodes": 1,
        "PossibleValues": [
          "ve1",
          "ve2"
        ],
        "HasSetSubnodes": 1,
        "AllowUnSet": 1,
        "HasUnSetSubnodes": 1,
        "Name": "%IF",
        "Description": "interface name",
        "HasSubnodes": 1,
        "MultiValue": 0,
        "Help": "<ifname.vlanid>"
      }
    ],
    "AllowUnSet": 0,
    "HasSetSubnodes": 1,
    "HasUnSetSubnodes": 1,
    "Name": "interface",
    "Description": "network interfaces",
    "HasSubnodes": 1
  }
}
```

## Expiration

The token expiration time is set to 30 min by default. It's possible to change the default value with `token-expiration`
command.

```
! set the lifetime of the token to 1 hour
netx# system user api-user api token-expiration 3600
```

## Obtain token via HTTP  

It's possible to obtain token remotely via HTTP request. However, an user requesting a token must have a valid password set.

* To obtain a token via HTTP, the user must provide valid credentials. Token is returned as JSON object. You can use /token
for 

```
curl -k -L https://<netx-address>/token -u username:password
{"token":"eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE1MzkxOTMxODcsImlhdCI6MTUzOTE5MTM4NywibmJmIjoxNTM5MTkxMzg3LCJ1c2VyIjoiYWRtaW4ifQ.RBLtMQ7DN3N1UUcZRZjysSuAotkyxyQQ6khwICEey60LJTxBd5aM0z-_ls0spw-C5NjyQnUUWst33iM6Xh5w4g"}
```

## Refresh a token

Tokens are by definition stateless, thus refreshing is quite easy - you just create a new one via REST API! In the following
example we use `create-token` command for our api-user.

```
curl -k -X POST https://<netx-address>/api-oauth/system/user/api-user/api/create-token -H "Authorization: Bearer eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE1MzkxOTM3MjIsImlhdCI6MTUzOTE5MTkyMiwibmJmIjoxNTM5MTkxOTIyLCJ1c2VyIjoiYXBpLXVzZXIifQ.Cu8h6YaE1cpiCR7pjCN54n3kzddY4Wh-4tPr9rG3q1WYe3tmq36-52gXyQ9PxykkgDBhkZ6hoICFxWm7354hVw" | jq .

{
  "RequestStatus": "OK",
  "Message": [
    "eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE1MzkxOTQwMDgsImlhdCI6MTUzOTE5MjIwOCwibmJmIjoxNTM5MTkyMjA4LCJ1c2VyIjoiYXBpLXVzZXIifQ.dnHMHEg7SEEZFLvtM63NIR_GsFSrb-e2-tJ-r-8vkAgO82-GOLwWf6xvCO3u4Wvvz5QFH_MpyzX6I2nF1ViHgA",
    "\n"
  ],
  "Request": {
    "Node": [
      "system",
      "user",
      "api-user",
      "api",
      "create-token"
    ],
    "PostData": {}
  }
}
```
