import json
import binascii

from client.network_connection.MessageConstants import *


##
# Manages a connection on the server side of a peer including the sending of data to a client
#
# @author Paul Rachwalski
# @date Apr 7, 2015
##
class ServerConnection(object):

    ##
    # Initializes the ServerConnection with the given network connection
    #
    # @param connection The network connection
    ##
    def __init__(self, connection):
        self.connection = connection
        return

    ##
    # Closes the network connection
    ##
    def terminate(self):
        if self.connection is not None:
            self.connection.close()
        return

    ##
    # Serves a section of of the file
    #
    # @param file The file path
    # @param file_id The file's universal id
    # @param offset The offset to the data in the file
    # @param length The length of the file
    ##
    def send_response(self, file, file_id, offset, length):
        metadata, data = ServerConnection.create_response(file, file_id, offset, length)
        meta_size = len(metadata.encode())
        total_size = meta_size + len(data)

        meta_size_str = "{:16d}".format(meta_size)
        total_size_str = "{:16d}".format(total_size)

        print("Uploader response: ", total_size_str, meta_size_str, metadata, data)

        message_str = total_size_str + meta_size_str + metadata
        self.connection.sendall(message_str.encode())
        self.connection.sendall(data)
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
    def create_response(file, file_id, offset, length):
        with open(file, "rb") as data_file:
            data_file.seek(offset)
            data_bytes = data_file.read(length)

        response_dict = {
            TYPE: TYPE_DATA,
            FILE: file_id,
            OFFSET: offset,
            SIZE: length
        }
        return json.dumps(response_dict), data_bytes