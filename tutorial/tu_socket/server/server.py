"""
A server that receives a message in json from the client via UDP connection on localhost:5005
"""

import socket 
import json 

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 5005)

# bind the socket to the port
sock.bind(server_address)

while True:
    print("Waiting for a message...")

    # receive data from client
    data, address = sock.recvfrom(4)

    print("Received %s bytes from %s" % (len(data), address))

    try:    
        data = json.loads(data.decode())
        print(data)
    except:
        print("Error: data is not in json format")

    if data:
        # send data back to client (in this scenario, the server echoes the message)
        sent = sock.sendto(data.encode(), address)
        print("Sent %s bytes back to %s" % (sent, address))