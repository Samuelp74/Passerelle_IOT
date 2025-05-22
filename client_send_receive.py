import socket
import sys
import json

HOST, PORT = "10.42.239.181", 10000
data = json.dumps({"action":"getValues()"})

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(data.encode(), (HOST, PORT))
received = sock.recv(1024)

print("Sent:     {}".format(data))
print("Received: {}".format(received.decode()))