import unittest
import json
import network_connection as nc
from network_connection import ClientConnection


##
# Test the ClientConnection class for the P2P functionality
# NOTE: To execute tests, run echo_server.py, and then run this file
#
# @author Paul Rachwalski
# @date Apr 2, 2015
##
class TestClientConnection(unittest.TestCase):

    def setUp(self):
        pass

    ##
    # Test that the create_request function works properly
    ##
    def test_message(self):
        file_id = "hi-123-2"
        offset = 12
        length = 4

        message = ClientConnection.create_request(file_id, offset, length)
        request = json.loads(message)

        self.assertEqual(nc.TYPE_REQUEST, request[nc.TYPE], "Incorrect message type")
        self.assertEqual(file_id, request[nc.FILE], "Incorrect file id")
        self.assertEqual(offset, request[nc.OFFSET], "Incorrect offset")
        self.assertEqual(length, request[nc.SIZE], "Incorrect length")

        return

    ##
    # Test that the sending of a request works properly using the echo_server
    ##
    def test_socket(self):
        client = ClientConnection("", 50000)

        file_id = "hi-123-2"
        offset = 12
        length = 4

        message_sent = client.send_request(file_id, offset, length)

        message_gen = json.loads(client.create_request(file_id, offset, length))

        self.assertEqual(message_gen, message_sent, "Incorrect message sent")

        return