# DNS App

This is the dns-app specified in Lab3 Q2. There are three servers:

- User servser (US)
  
    A HTTP server running on localhost:8080
  
    Listening to 
  
  - HTTP GET requests on `/`
  
  - HTTP GET requests on `/fibonacci`

- Fibonacci server (FS)
  
    A HTTP server running on localhost:9090
  
    Listening to 
  
  - HTTP GET requests on `/fibonacci`
  
  - HTTP POST requests on `/register`
    
      When a POST request is received, the server will register the client's IP address and port number to the DNS server using UDP socket.    

- Authoritative server (AS)
  
    A DNS server running on localhost:53533 (a UDP socket that accepts messages and replies to them)
  
    Listening to
  
  - messages (in json format) from other servers
    
    The format of messages is specified in `FS/README.md`

Each server is running on a docker container. 

## How to build docker images

### AS

To build the docker image for AS, run the following command in the root directory of this project:

```bash
cd AS/
docker build -t dns-app/as .
```

### FS

To build the docker image for FS, run the following command in the root directory of this project:

```bash
cd FS/
docker build -t dns-app/fs .
```

### US

To build the docker image for US, run the following command in the root directory of this project:

```bash
cd US/
docker build -t dns-app/us .
```

## How to run applications on docker containers locally on your machine

Note that the servers must be started in the following order: **AS, FS, US**.

For convenience, we will run containers with `--network=host`, so that the containers run on the host network instead of a virtual network. This means that the container shares the same network stack as the host machine and can access all its network interfaces and ports.

### AS

To run the authoritative server on a docker container, run the following command:

```bash
docker run -t --network=host dns-app/as
```

### FS

To run the fibonacci server on a docker container, run the following command:

```bash
docker run -t --network=host dns-app/fs
```

### US

To run the user server on a docker container, run the following command:

```bash
docker run -t --network=host dns-app/us
```

## How to access the user server

To access the user server, open a browser and go to the following url 

```javascript
http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=12&as_ip=localhost&as_port=53533
```

This will give you the 12nd fibonacci number.

## How to update DNS record

To create / update the DNS record of the Fibonacci server, one can send a HTTP PUT request to fibonacci server at "/register". 

An example is given in `FS/register_dns.py`, where a HTTP PUT request is sent to FS at `localhost:9090` using the python `requests` package. 
