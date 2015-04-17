import unittest
import socket
import json

from client import network_connection as nc
from client.network_connection import ServerConnection



##
# Test the ServerConnection class for the P2P functionality
# NOTE: To execute tests, run this file, and then run simple_client.py
#
# @author Paul Rachwalski
# @date Apr 2, 2015
##
class TestServerConnection(unittest.TestCase):

    def setUp(self):
        pass

    def test_message(self):
        file = "data/a.txt"
        file_id = "hi-123-2"
        offset = 0
        length = 4

        message = ServerConnection.create_response(file, file_id, offset, length)
        request = json.loads(message)

        self.assertEqual(nc.TYPE_DATA, request[nc.TYPE], "Incorrect message type")
        self.assertEqual(file_id, request[nc.FILE], "Incorrect file id")
        self.assertEqual(offset, request[nc.OFFSET], "Incorrect offset")
        self.assertEqual(length, request[nc.SIZE], "Incorrect length")
        self.assertEqual(len(request[nc.DATA].encode()), 4, "Incorrect amount of data")

        return

    def test_socket(self):
        file = "data/a.txt"
        file_id = "hi-123-2"
        offset = 0
        length = 4

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", 50001))
        s.listen(1)

        connection, address = s.accept()
        server = ServerConnection(connection)

        self.assertTrue(connection.recv(1024) is not None, "Initial connection sent no data")
        server.send_response(file, file_id, offset, length)
        data = connection.recv(1024).decode()
        self.assertEqual(data, ServerConnection.create_response(file, file_id, offset, length),
                         "Server connection did not send proper data")

        s.close()
        return