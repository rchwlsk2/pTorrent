import socket
import json

from client.network_connection.MessageConstants import *
import client.CONSTANTS as CONSTANTS



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
        if self.ip == CONSTANTS.LOCALHOST:
            self.ip = ""

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
        return

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
    #
    # @param file_id The ID of the file to download
    # @param offset The offset of the piece of the file to get
    # @param length The size of the piece of the file to get
    ##
    def send_request(self, file_id, offset, length):
        message = ClientConnection.create_request(file_id, offset, length)
        self.sock.send(message.encode())
        print("Sent request json:", message)

        # Read entire response
        total_size = int(self.sock.recv(16).decode())
        meta_size = int(self.sock.recv(16).decode())
        print("Received total size: ", total_size, " meta size: ", meta_size)

        response = b""
        while total_size:
            part = self.sock.recv(CONSTANTS.BUFFER_SIZE)
            if not part:
                continue
            response += part
            total_size -= len(part)
        metadata = response[:meta_size].decode()
        byte_data = response[meta_size:]

        print("Received", metadata, byte_data)

        # Check that response is proper
        if response:
            response_dict = json.loads(metadata)
            same_id = response_dict[FILE] == file_id
            same_offset = response_dict[OFFSET] == offset
            same_length = response_dict[SIZE] == length
            if same_id and same_offset and same_length:
                return response_dict, byte_data

        return None

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