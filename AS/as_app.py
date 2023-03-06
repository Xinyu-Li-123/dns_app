"""
This is the program for Authorirative Server (AS).

AS uses sqlite to store the DNS records, and uses UDP to communicate with other servers.

"""
import socket 
import sqlite3
import json

def _connect_db():
    """
    Connect to the database
    """
    conn = sqlite3.connect("dns.db")
    return conn


def _init_db():
    """
    Initialize the database
    """
    conn = _connect_db()
    c = conn.cursor()
    # c.execute("CREATE TABLE IF NOT EXISTS dns (name TEXT, value TEXT, type TEXT, ttl INTEGER)")
    # create a table to store the DNS records where name is the primary key
    c.execute("CREATE TABLE IF NOT EXISTS dns (name TEXT PRIMARY KEY, value TEXT, type TEXT, ttl INTEGER)")
    conn.commit()
    conn.close()


def _validate_request(data):
    """
    Check if request is of valid format based on its action type
    """
    if not data:
        return False, "Not a valid JSON object."
    elif data["action"] == "register":
        if not data.get("name") or not data.get("value") or not data.get("type") or not data.get("ttl"):
            return False, "Missing parameters"
        else:
            return True, ""
    elif data["action"] == "lookup":
        if not data.get("name") or not data.get("type"):
            return False, "Missing parameters"
        else:
            return True, ""
    else:
        return False, "Invalid action"


def _register_handler(data):
    """
    Handle register request. Return a json object
    """
    conn = _connect_db()
    c = conn.cursor()
    # if the name already exists, update the record
    c.execute("SELECT * FROM dns WHERE name=?", (data["name"],))
    result = c.fetchone()
    if result:
        c.execute("UPDATE dns SET value=?, type=?, ttl=? WHERE name=?", (data["value"], data["type"], data["ttl"], data["name"]))
    else:
        c.execute("INSERT INTO dns VALUES (?, ?, ?, ?)", (data["name"], data["value"], data["type"], data["ttl"]))
    # c.execute("INSERT INTO dns VALUES (?, ?, ?, ?)", (data["name"], data["value"], data["type"], data["ttl"]))
    conn.commit()
    conn.close()
    return {
        "action": data["action"],
        "status": True,
        "message": "Successfully registered"
    }


def _lookup_handler(data):
    """
    Handle lookup request. Return a json object
    """ 
    conn = _connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM dns WHERE name=? AND type=?", (data["name"], data["type"]))
    result = c.fetchone()
    conn.close()
    if result:
        return {
            "action": data["action"],
            "status": True,
            "name": result[0],
            "value": result[1],
            "type": result[2],
            "ttl": result[3]
        }
    else:
        return {
            "action": data["action"],
            "status": False,
            "message": "Name not found"
        }


def run():

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 53533)
    sock.bind(server_address) 

    print("Authoritative Server is running on {}:{} ..." .format(
        server_address[0], server_address[1]))

    while True:
        data, address = sock.recvfrom(4096)
        print("Received %s bytes from %s" % (len(data), address))

        # parse the data
        data = json.loads(data)
        
        # validate the request
        is_valid, message = _validate_request(data)

        if not is_valid:
            print("Invalid request: {}" .format(message))
            response = {
                "action": data["action"],
                "status": False,
                "message": message
            }
            sock.sendto(json.dumps(response).encode(), address)
            continue
        else:
            if data["action"] == "register":
                print("Registering...")
                response = _register_handler(data)
                if response["status"]:
                    print("Registered successfully")
                else:
                    print("Failed to register: {}".format(
                        response["message"]
                        ))
            elif data["action"] == "lookup":
                print("Looking up hostname...")
                response = _lookup_handler(data)
                if response["status"]:
                    print("Lookup successful")
                else:
                    print("Failed to lookup: {}".format(
                        response["message"]
                        ))
            else:
                print("Invalid action")
                response = {
                    "action": data["action"],
                    "status": False,
                    "message": "Invalid action"
                }
            sock.sendto(json.dumps(response).encode(), address)

_init_db()
run()