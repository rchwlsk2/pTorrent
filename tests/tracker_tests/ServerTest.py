import unittest
import socket
from tracker.TrackerConstants import TrackerConstants


##
# Semi-manual testing to test that the server returns the proper values
#
# NOTE: Prior to running, must run a TrackerServer instance from terminal
#
# @author Paul Rachwalski
# @date Apr 3, 2015
##
class TestServer(unittest.TestCase):

    DB_PATH = "../data/test_tracker.db"
    DB_SCHEMA = "../data/schema.sql"

    sample_vals = (("abcd", "123.456.8.3"), ("SDFGHS", "123.456.8.3"), ("SDFGHS", "342.455.531.84"))

    def setUp(self):
        pass

    ##
    # Test adding and removing a single value
    ##
    def test_manual_single_data(self):
        print("one data")

        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect to server
        s.connect(('', 6044))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.CONNECT_SUCCESS)

        # Test GET on empty db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.GET_FAIL, "Incorrect response for empty GET query")

        # Test ADD on empty db
        query = TrackerConstants.ADD + self.sample_vals[0][0] + " " + self.sample_vals[0][1]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.ADD_SUCCESS, "Incorrect response for single ADD query")

        # Test GET on single-value db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, self.sample_vals[0][1], "Incorrect response for single GET query")

        # Test REM on empty db
        query = TrackerConstants.REMOVE + self.sample_vals[0][0] + " " + self.sample_vals[0][1]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.REMOVE_SUCCESS, "Incorrect response for single REM query")

        # Test GET on empty db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.GET_FAIL, "Incorrect response for empty GET query")

        s.close()
        return

    ##
    # Test adding several values and using multiple removal
    ##
    def test_manual_multiple_data(self):
        print("multi data")

        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect to server
        s.connect(('', 6044))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.CONNECT_SUCCESS)

        # Test GET on empty db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.GET_FAIL, "Incorrect response for empty GET query")

        # Test ADD on empty db
        query = TrackerConstants.ADD + self.sample_vals[0][0] + " " + self.sample_vals[0][1]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.ADD_SUCCESS, "Incorrect response for first ADD query")

        query = TrackerConstants.ADD + self.sample_vals[1][0] + " " + self.sample_vals[1][1]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.ADD_SUCCESS, "Incorrect response for second ADD query")

        # Test GET on single-value db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, self.sample_vals[0][1], "Incorrect response for single GET query")

        # Test REM on empty db
        query = TrackerConstants.REMOVE + "* " + self.sample_vals[0][1]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.REMOVE_SUCCESS, "Incorrect response for single REM query")

        # Test GET on empty db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        s.send(str.encode(query))
        data = s.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.GET_FAIL, "Incorrect response for empty GET query")

        s.close()
        return

    ##
    # Test multiple connections
    ##
    def test_manual_multiple_conn(self):
        print("multi conn")

        # Create sockets
        sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sa.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect to server
        sa.connect(('', 6044))
        data = sa.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.CONNECT_SUCCESS)

        sb.connect(('', 6044))
        data = sb.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.CONNECT_SUCCESS)

        # Test GET on empty db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        sa.send(str.encode(query))
        data = sa.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, TrackerConstants.GET_FAIL, "Incorrect response for empty GET query")

        # Test ADD on empty db
        query = TrackerConstants.ADD + self.sample_vals[0][0] + " " + self.sample_vals[0][1]
        sa.send(str.encode(query))
        data = sa.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.ADD_SUCCESS, "Incorrect response for first ADD query")

        # Test GET on single-value db
        query = TrackerConstants.GET + self.sample_vals[0][0]
        sb.send(str.encode(query))
        data = sb.recv(1024)
        data = bytes.decode(data)
        self.assertEqual(data, self.sample_vals[0][1], "Incorrect response for single GET query")

        # Test REM on empty db
        query = TrackerConstants.REMOVE + "* " + self.sample_vals[0][1]
        sb.send(str.encode(query))
        data = sb.recv(1024)
        data = bytes.decode(data)
        print(data)
        self.assertEqual(data, TrackerConstants.REMOVE_SUCCESS, "Incorrect response for single REM query")

        sa.close()
        sb.close()
        return
