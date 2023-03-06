# User Server

Below is an example that specifies
- a fibonacci server by hostname:port (localhost:53533)
- sequence number of the fibonacci number (12)
- an authoritative server by ip:port (fibonacci.com:9090) to lookup the hostname

```url
http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=12&as_ip=localhost&as_port=53533
```