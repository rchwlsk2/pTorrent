#!/usr/bin/env python

##
# A simple echo server
##

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',50000))
s.listen(1)

client, address = s.accept()
data = client.recv(1024)
if data:
    client.send(data)
client.close()