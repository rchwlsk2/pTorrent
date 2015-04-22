import socket

from client.network_connection import ClientConnection


# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

file = "a.txt-128-32"
offset = 128
length = 32

# Connect to server
s.connect(('', 50001))
s.send(ClientConnection.create_request(file, offset, length).encode())

data = s.recv(1024)
s.send(data)

s.close()