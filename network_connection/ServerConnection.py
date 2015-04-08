import json
from network_connection.MessageConstants import *

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
        message = ServerConnection.create_response(file, file_id, offset, length)
        self.connection.send(message.encode())
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
            data_bytes = data_file.read(length).decode()

        response_dict = {
            TYPE: TYPE_DATA,
            FILE: file_id,
            OFFSET: offset,
            SIZE: length,
            DATA: data_bytes
        }
        return json.dumps(response_dict)