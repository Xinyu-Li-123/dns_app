import flask 
import socket
import json

app = flask.Flask("Fibonacci server")

def _fib(X):
    # calculate fibonacci number using while loop
    a, b = 0, 1
    while X > 0:
        a, b = b, a + b
        X -= 1
    return a

@app.route("/")
def index():
    return "Hello from the fibonacci server!"


@app.route("/register", methods=["PUT"])
def register():
    """
    Accept HTTP PUT request at /register, and
    create UDP socket to send a DNS register message to AS
    
    The DNS message body is a JSON object with the following fields:
    - hostname: hostname of fibonacci server
    - ip: ip address of fibonacci server
    - as_ip: ip address of authoritative server
    - as_port: port of authoritative server

    if registration is successful, return "201 OK"
    else return "400 Bad Request" and error message from the AS
    """
    # TODO: 
    # [v] 1. parse request body
    # ]v] 2. validate request body
    # [v] 3. register the server to AS via UDP on port 53533
    #   DNS message: (Name, Value, Type, TTL)
    # [v] 4. return "201 OK" if success, and 400 if fail

    # accept only PUT request
    if flask.request.method != "PUT":
        print("Method {} not allowed! Please use PUT request.".format(
            flask.request.method
        ))
        flask.abort(405, "Method not allowed! Please use PUT request.")
    
    # parse request body
    try:
        body = flask.request.get_json()
    except:
        flask.abort(400, "Bad request! Please specify a valid JSON object.")
    
    # validate request body
    _validate_register(body)

    # register FS to AS via UDP on port 53533 (send a DNS message to AS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (body["as_ip"], int(body["as_port"]))
    message = {
        "action": "register",
        "type": "A",
        "name": body["hostname"],
        "value": body["ip"],
        "ttl": 3600
    }
    sock.sendto(json.dumps(message).encode(), server_address)

    # receive response from AS
    data, address = sock.recvfrom(4096)
    print("Received %s bytes from %s" % (len(data), address))
    
    # jsonify the response
    data = json.loads(data.decode())

    if data["status"]:
        # response user with HTTP 201 OK
        return flask.make_response("201 OK", 201)
    else:
        # response user with HTTP 400 Bad Request
        flask.abort(400, data["message"])


def _validate_register(body):
    if not body:
        flask.abort(400, "Bad request! Please specify a valid JSON object.")

    if not body.get("hostname"):
        flask.abort(400, "Bad request! Please specify a hostname.")
    
    if not body.get("ip"):
        flask.abort(400, "Bad request! Please specify an ip address.")

    if not body.get("as_ip"):
        flask.abort(400, "Bad request! Please specify an AS ip address.")
    
    if not body.get("as_port"):
        flask.abort(400, "Bad request! Please specify an AS port.")
    

@app.route("/fibonacci")
# /fibonacci?number=X
def fibonacci():
    number = flask.request.args.get("number")
    if not number:
        flask.abort(400, "Bad request! Please specify a number.")
    try:
        number = int(number)
    except ValueError:
        flask.abort(400, "Bad request! Argument number must be a valid integer.")
    
    if number < 0:
        flask.abort(400, "Bad request! Argument number must be nonnegative integer.")

    return str(_fib(number))

app.run(port=9090)