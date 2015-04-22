import socket
import threading
import client.CONSTANTS as CONSTANTS
from tracker.TrackerConstants import *


##
# Keeps track of a connection to the tracker
#
# @author Paul Rachwalski
# @date Apr 21, 2015
##
class TrackerThread(threading.Thread):

    ##
    # Initializes socket connection
    #
    # @param tracker_ip The IP address of the tracker
    # @param tracker_port The port to connect to on the tracker
    ##
    def __init__(self, tracker_ip, tracker_port):
        super().__init__(group=None, target=None, name=None, args=(), kwargs={})

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.connect((tracker_ip, tracker_port))
        except socket.error as sockerr:
            print("Could not connect to tracker at " + tracker_ip + ":" + tracker_port + " --- " + sockerr.strerror)
            return

        self.cv = threading.Condition()
        self.should_run = True

        return

    ##
    # Keeps socket from closing
    ##
    def run(self):
        while self.should_run:
            with self.cv:
                self.cv.wait()
        self.sock.close()
        self.sock = None
        return

    ##
    # Closes socket if possible
    ##
    def stop(self):
        if not self.sock:
            return

        self.should_run = False
        with self.cv:
            self.cv.notify()
        return

    ##
    # Adds a file reference to the tracker server
    #
    # @param file_id The ID of the file to add
    # @param ip The IP address to add
    # @param port The port to add
    ##
    def add(self, file_id, ip, port):
        if not self.sock:
            return None

        query = TrackerConstants.ADD + file_id + " " + ip + " " + str(port)
        self.sock.sendall(query.encode())
        result = self.sock.recv(CONSTANTS.BUFFER_SIZE)
        return result

    ##
    # Removes a file reference from the tracker server
    #
    # @param file_id The ID of the file to remove
    # @param ip The associated IP address with the file
    ##
    def remove(self, file_id, ip):
        if not self.sock:
            return None

        query = TrackerConstants.REMOVE + file_id + " " + ip
        self.sock.sendall(query.encode())
        result = self.sock.recv(CONSTANTS.BUFFER_SIZE)
        return result

    ##
    # Removes all file references for an ip on the tracker server
    #
    # @param ip The IP address to remove
    ##
    def remove_all(self, ip):
        if not self.sock:
            return None

        query = TrackerConstants.REMOVE + "* " + ip
        self.sock.sendall(query.encode())
        result = self.sock.recv(CONSTANTS.BUFFER_SIZE)
        return result