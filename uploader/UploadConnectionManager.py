import threading
from network_connection import ServerConnection, MessageConstants


##
# Keeps track of connections for uploading files
#
# @author Paul Rachwalski
# @date Apr 14, 2015
##
class UploadConnectionManager(object):

    ##
    # Initialize the connection dictionary
    #
    # @param
    ##
    def __init__(self, download_mgr):
        self.download_mgr = download_mgr

        # Key is (ip, port) tuple, value is connection thread
        self.connections = {}
        return

    ##
    # Creates a new connection if one does not exist
    #
    # @param ip The IP address of the connection
    # @param port The port of the connection
    ##
    def add(self, ip, port):
        if (ip, port) not in self.connections:
            connection = UploadConnectionThread(self, ip, port)
            self.connections[(ip, port)] = connection
            connection.start()
        return

    ##
    # Gets the proper connection for a provided IP address and port
    #
    # @param ip The IP address of the connection
    # @param port The port of the connection
    # @return The corresponding connection thread, if it exists
    ##
    def get(self, ip, port):
        return self.connections[(ip, port)]


##
# Extension of Thread class to be able to process requests to a given IP address
##
class UploadConnectionThread(threading.Thread):

    ##
    # Extends default constructor to store the ip and port of the file host
    #
    # @param download_mgr The DownloadManager of that owns the DCM
    # @param ip The IP address of the host
    # @param port The port of the host
    ##
    def __init__(self, download_mgr, ip, port):
        super().__init__(group=None, target=None, name=None, args=(), kwargs={})

        self.download_mgr = download_mgr
        self.ip = ip
        self.port = port

        self.cv = threading.Condition()     # Condition variable to signal when a thread should send a request
        self.requests = []              # Queue of requests to process (request is (file_id, offset, piece_size) tuple)
        return

    ##
    # Function that a user calls to request a piece of a file
    #
    # @param request The request tuple of the form (file_id, offset, piece_size)
    ##
    def request(self, request):
        self.requests.append(request)
        with self.cv:
            self.cv.notify()
        return

    ##
    # Overrides the default run function to queue downloads
    ##
    def run(self):
        print("DOWNLOAD THREAD: ", self.ip, self.port)
        client_conn = ServerConnection(self.ip, self.port)

        while True:
            self.cv.acquire()
            while len(self.requests) == 0:
                self.cv.wait()
            self.cv.release()

            request = self.requests.pop()
            response = self.client_conn.send_request(request[0], request[1], request[2])

            if not response:
                continue
            else:
                self.download_mgr.send_to_downloader(self.ip, response)

        client_conn.terminate()
        return