import unittest
import socket
import json

from client import network_connection as nc
from client.network_connection import ServerConnection



##
# Test the ServerConnection class for the P2P functionality
# NOTE: To execute tests, run this file, and then run server_test_client.py
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

        message, data = ServerConnection.create_response(file, file_id, offset, length)
        request = json.loads(message)

        self.assertEqual(nc.TYPE_DATA, request[nc.TYPE], "Incorrect message type")
        self.assertEqual(file_id, request[nc.FILE], "Incorrect file id")
        self.assertEqual(offset, request[nc.OFFSET], "Incorrect offset")
        self.assertEqual(length, request[nc.SIZE], "Incorrect length")

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

        gen_meta, gen_data = ServerConnection.create_response(file, file_id, offset, length)
        gen_meta = json.loads(gen_meta)

        self.assertTrue(connection.recv(1024) is not None, "Initial connection sent no data")
        server.send_response(file, file_id, offset, length)

        total_size = int(connection.recv(16).decode())
        meta_size = int(connection.recv(16).decode())

        response = b""
        while total_size:
            part = connection.recv(1024)
            if not part:
                continue
            response += part
            total_size -= len(part)
        metadata = json.loads(response[:meta_size].decode())
        byte_data = response[meta_size:]

        self.assertEqual(metadata[nc.FILE], gen_meta[nc.FILE],
                         "Server connection did not send proper file id")
        self.assertEqual(metadata[nc.OFFSET], gen_meta[nc.OFFSET],
                         "Server connection did not send proper file offset")
        self.assertEqual(metadata[nc.SIZE], gen_meta[nc.SIZE],
                         "Server connection did not send proper file piece size")
        self.assertEqual(byte_data, gen_data,
                         "Server connection did not send proper file byte data")

        connection.close()
        s.close()
        return