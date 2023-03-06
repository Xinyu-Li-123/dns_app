# DNS Message Format for Authoritative Server

There are two types of DNS messages: request and response

We only implement type-A record and the following types of requests and responses:

## Registration

Register a DNS record to the DNS database.

```python 
request = {
    "action": "register",
    "type": "A",
    "name": hostname,
    "value": ip_address,
    "ttl": "3600
}

response = {
    "action": "register",
    "status": True | False,
    "message": "OK" | "Error Message"
}
```

Error message can be one of the following:
```python
"Invalid type"     # invalid type
"Invalid value (IP)" # invalid IP address
"Invalid TTL"      # invalid TTL
```

## DNS lookup

lookup the DNS database

```python
request = {
    "action": "lookup",
    "type": "A",
    "name": hostname
}

if response["status"] == True:
    response = {
        "action": "lookup",
        "status": True,
        "name": hostname,
        "value": ip_address,
        "type": "A",
        "ttl": "3600"
    }
else:
    response = {
        "action": "lookup",
        "status": False,
        "message": "Error Message"
    }
```

The error message can be one of the following:

```python
"Invalid type"     # invalid type

"Name not found"   # hostname not found
```