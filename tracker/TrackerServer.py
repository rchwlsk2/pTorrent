from socket import *
from socket import error as sock_err
import threading
import os
import signal
import sys

from TrackerConstants import *
from DatabaseManager import DatabaseManager

##
# A simple tracker server for the pTorrent project
#
# @author Paul Rachwalski
# @date Apr 2, 2015
##
class TrackerServer(object):

    ##
    # Initializes a socket corresponding to the host and port
    #
    # @param host The IP of the host
    # @param port The port # of the server
    # @param db_schema The absolute path to the database schema
    # @param db_path The absolute path to the database file
    ##
    def __init__(self, host, port, db_schema, db_path):
        self.host = host
        self.port = port
        self.buffer_size = 1024

        self.db_path = db_path
        self.db_schema = db_schema
        print(self.db_path, self.db_schema)

        self.db_manager = DatabaseManager(self.db_schema, self.db_path)
        if not os.path.exists(self.db_path):
            self.db_manager.init_db()

        # Exit handler
        signal.signal(signal.SIGINT, self.exit_handler)

        # Make sure localhost runs properly
        if host == LOCALHOST:
            host = ""

        address = (host, port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        print("Starting server... ")
        try:
            self.sock.bind(address)
        except sock_err as e:
            print('Socket bind failed. Error Code: ' + str(e))
            sys.exit()

        hostname = host if host != '' else "localhost"
        print("Server is running at " + hostname + ":" + str(port) + "\n")
        self.sock.listen(10)

        # Start the server loop
        self.server_loop()

        self.sock.close()
        return

    ##
    # Exit SIGINT handler (ctrl+c)
    ##
    def exit_handler(self, signum, frame):
        print("\nServer stopped!")
        sys.exit(0)

    ##
    # The loop of the server to accept connections
    ##
    def server_loop(self):
        while True:
            connection, address = self.sock.accept()
            print('Connected with ' + address[0] + ':' + str(address[1]))

            threading.Thread(target=self.client_thread, args=(connection,)).start()
        return

    ##
    # Thread for handling each individual connection
    #
    # @param connection The connection to the client
    ##
    def client_thread(self, connection):
        connection.send(str.encode(TrackerConstants.CONNECT_SUCCESS))

        while True:
            data = connection.recv(self.buffer_size)
            if not data:
                return

            data = bytes.decode(data)
            if data.startswith(TrackerConstants.ADD):
                data = data[len(TrackerConstants.ADD):]
                split = data.split(" ")
                if len(split) == 3:
                    self.db_manager.add(split[0], split[1], split[2])
                    connection.send(str.encode(TrackerConstants.ADD_SUCCESS))
                else:
                    connection.send(str.encode(TrackerConstants.ADD_FAIL))

            elif data.startswith(TrackerConstants.REMOVE):
                data = data[len(TrackerConstants.REMOVE):]
                split = data.split(" ")
                if len(split) == 2:
                    self.db_manager.remove(split[0], split[1])
                    connection.send(str.encode(TrackerConstants.REMOVE_SUCCESS))
                else:
                    connection.send(str.encode(TrackerConstants.REMOVE_FAIL))

            elif data.startswith(TrackerConstants.GET):
                data = data[len(TrackerConstants.GET):]
                ips = self.db_manager.get(data)
                if len(ips) > 0:
                    ip_str = ""
                    for pair in ips:
                        ip_str += pair[0] + ":" + str(pair[1]) + "-"
                    connection.send(str.encode(ip_str.strip("-")))
                else:
                    connection.send(str.encode(TrackerConstants.GET_FAIL))

        connection.close()
        return