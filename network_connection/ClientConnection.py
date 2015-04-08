import socket
import json
from network_connection.MessageConstants import *


##
# Manages a connection on the client side of a peer including requesting data from file hosts
#
# @author Paul Rachwalski
# @date Apr 7, 2015
##
class ClientConnection(object):

    ##
    # Creates a new socket connection to the desired IP address and port
    #
    # @param ip The IP address of the file host
    # @param port The port number to connect to on the file host
    ##
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        # Initialize socket
        self.sock = None
        self.initialize()
        return

    ##
    # Initializes the socket to the designated IP and port
    ##
    def initialize(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.ip, self.port))

    ##
    # Closes the network connection
    ##
    def terminate(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        return

    ##
    # Requests a section of of the file
    ##
    def send_request(self, file, file_id, offset, length):
        message = ClientConnection.create_request(file_id, offset, length)
        self.sock.send(message.encode())
        return


    ##
    # Creates a JSON string for the response message
    #
    # @param file The file path
    # @param file_id The file's universal id
    # @param offset The offset to the data in the file
    # @param length The length of the file
    # @return The JSON string of the message
    ##
    @staticmethod
    def create_request(file_id, offset, length):
        response_dict = {
            TYPE: TYPE_REQUEST,
            FILE: file_id,
            OFFSET: offset,
            SIZE: length
        }

        return json.dumps(response_dict)