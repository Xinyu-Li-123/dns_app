import flask 

# User server (US)
app = flask.Flask("User server")

@app.route("/")
def index():
    return "Hello from the user server!"

# user can access via
# /fibonacci?
#   hostname=fibonacci.com&
#   fs_port=K&
#   number=X&
#   as_ip=Y&
#   as_port=Z
@app.route("/fibonacci")
def fibonacci():
    """
    There are five parameters
    hostname: hostname of Fibonacci Server (FS)
    fs_port: port of FS
    number: ask FS to calculate the Xth fibonacci number
    as_ip: ip of Authoritative Server (AS)
    as_port: port of AS
    """
    # n = int(flask.request.args.get("n", 0))
    # return str(fib(n))
    hostname = flask.request.args.get("hostname")
    fs_port = flask.request.args.get("fs_port")
    number = flask.request.args.get("number")
    as_ip = flask.request.args.get("as_ip")
    as_port = flask.request.args.get("as_port")
    is_request_valid = hostname and fs_port and number and as_ip and as_port

    if not is_request_valid:
        flask.abort(400, 'Bad Request >:(')
    else:
        # request AS to convert fs_hostname to fs_ip
        # request fs_ip/fibonacci?number=X
        # return result
        pass 

    return "<h1>Well Done</h1>Good job :)"



def fib(n):
    # calculate fibonacci number using while loop
    a, b = 0, 1
    while n > 0:
        a, b = b, a + b
        n -= 1
    return a

app.run(port=8080)


