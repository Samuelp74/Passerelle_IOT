import socket
import sys
import json

HOST, PORT = "localhost", 10000
data = json.dumps({"command":"HTL"})

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(data.encode(), (HOST, PORT))