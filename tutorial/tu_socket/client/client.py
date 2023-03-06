"""
A client that send a message in json to the server via UDP connection on localhost:5005
"""

import socket
import json 
import time

# create UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    server_address = ('localhost', 5005)

    client_address = ('localhost', 5006)

    # bind the socket to the port
    sock.bind(client_address)

    print("Client is running on {}:{}" .format(*client_address))

    # while True:
    #     message = input("Enter message: ")
    #     message = json.dumps(message)
    #     sock.sendto(message.encode(), server_address)

    #     data, address = sock.recvfrom(4096)
    #     print("Received %s bytes from %s" % (len(data), address))
    #     print(data.decode())

    for i in range(10):
        time.sleep(1)
        message = "Message {}".format(i)
        message = json.dumps(message)
        sock.sendto(message.encode(), server_address)

        data, address = sock.recvfrom(4096)
        print("Received %s bytes from %s" % (len(data), address))
        print(data.decode())
