import flask 
import socket
import json
import requests

# User server (US)
app = flask.Flask("User server")

@app.before_request
def before_request():
    print("Received request from {} at {}".format(
        flask.request.remote_addr, flask.request.url
    ))

@app.route("/")
def index():
    return "Hello from the user server!"


@app.route("/favicon.ico")
def favicon():
    return flask.send_file("favicon.ico")


@app.route("/fibonacci")
# user can request via the url:
# /fibonacci?
#   hostname=fibonacci.com&
#   fs_port=K&
#   number=X&
#   as_ip=Y&
#   as_port=Z
def fibonacci():
    """
    There are five parameters
    hostname: hostname of Fibonacci Server (FS)
    fs_port: port of FS
    number: ask FS to calculate the Xth fibonacci number
    as_ip: ip of Authoritative Server (AS)
    as_port: port of AS
    """
    hostname = flask.request.args.get("hostname")
    fs_port = flask.request.args.get("fs_port")
    number = flask.request.args.get("number")
    as_ip = flask.request.args.get("as_ip")
    as_port = flask.request.args.get("as_port")
    is_request_valid = hostname and fs_port and number and as_ip and as_port

    # if any parameter is missing, return 400 Bad Request
    if not is_request_valid:
        flask.abort(400, 'Please enter all 5 arguments (hostname, fs_port, number, as_ip, as_port)')
    else:
        # request AS to convert fs_hostname to fs_ip via UDP 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (as_ip, int(as_port))
        message = {
            "action": "lookup",
            "type": "A",
            "name": hostname
        }
        sock.sendto(json.dumps(message).encode(), server_address)

        # receive response from AS
        data, address = sock.recvfrom(4096)
        sock.close()

        # jsonify the response
        data = json.loads(data.decode())
        # if AS failed
        if not data["status"]:
            flask.abort(400, data["message"])
        # if AS succeeded
        else:
            fs_ip = data["value"]

            # request fs_ip/fibonacci?number=X via TCP and HTTP
            response = requests.get(
                f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
        
            # return the result fibonacci number and 200 OK
            if response.status_code == 200:
                return response.text
            else:
                flask.abort(response.status_code, response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


