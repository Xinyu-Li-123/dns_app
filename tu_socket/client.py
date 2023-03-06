"""
A client that send a message in json to the server via UDP connection on localhost:5005
"""

import socket
import json 

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 5005)

while True:
    message = input("Enter message: ")
    message = json.dumps(message)
    sock.sendto(message.encode(), server_address)

    data, address = sock.recvfrom(4096)
    print("Received %s bytes from %s" % (len(data), address))
    print(data.decode())
