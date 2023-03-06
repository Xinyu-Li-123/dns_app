import flask 

# User server (US)
app = flask.Flask("User server")

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
        flask.abort(400, 'Please enter all 5 arguments (hostname, fs_port, number, as_ip, is_request_valid)')
    else:
        # TODO:
        # request AS to convert fs_hostname to fs_ip
        # request fs_ip/fibonacci?number=X
        # return the result fibonacci number and 200 OK
        pass 

    return "<h1>Well Done</h1>Good job :)"


app.run(port=8080)


