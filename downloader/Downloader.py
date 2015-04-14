import threading
import socket
from file_manager import FileAssembler
from tracker import TrackerConstants
from network_connection import ClientConnection, MessageConstants
import CONSTANTS


##
# In charge of downloading a file from all available hosts
#
# @author Paul Rachwalski
# @date Apr 9, 2015
##
class Downloader(object):

    ##
    # Starts the download threads and the thread to keep the ip list up to date
    #
    # @param download_mgr The DownloadManager to use to interface with the connection manager
    # @param metadata The path to the metadata file
    ##
    def __init__(self, download_mgr, metadata, ip, port):
        self.download_mgr = download_mgr
        self.file = FileAssembler(metadata)
        self.file_id = self.file.metadata.file_id
        self.host = ip
        self.port = port

        self.ip_threads = {}
        self.ips = []

        self.should_wake = False
        self.cv = threading.Condition()     # Condition variable to prevent queueing of entire files immediately

        self.should_run = True
        return

    ##
    # Starts the download
    ##
    def start(self):
        self.should_run = True
        self.ip_refresh()
        return

    ##
    # Stops the download and saves the progress
    ##
    def stop(self):
        self.should_run = False
        return

    ##
    # Timer thread to periodically refresh the list of IP addresses to download from
    ##
    def ip_refresh(self):
        new_ips = []
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.should_run:
            print(self.file_id + " : refreshing")

            # Restart timer
            threading.Timer(CONSTANTS.UPDATE_INTERVAL, self.ip_refresh).start()

            # Send request to server
            message = TrackerConstants.GET + self.file_id
            print(message)

            sock.connect((self.host, self.port))
            response = sock.recv(CONSTANTS.BUFFER_SIZE).decode()
            if response == TrackerConstants.CONNECT_SUCCESS:
                sock.send(message.encode())
                ip_str = sock.recv(CONSTANTS.BUFFER_SIZE).decode()
                new_ips = ip_str.split(" ")
                print("Tracker response: " + str(new_ips))

            # Setup connection to tracker
            for ip in new_ips:
                if ip not in self.ips:
                    thread = threading.Thread(target=self.connection_thread, args=(ip, CONSTANTS.PORT))
                    self.ip_threads.append(thread)
                    self.download_mgr.conn_mgr.add(ip, CONSTANTS.PORT)
                    thread.start()

            for cur_thread in self.ip_threads:
                if cur_thread.ip not in new_ips:
                    cur_thread.exit()
                    new_ips.remove(cur_thread.ip)
                    self.ip_threads.remove(cur_thread)

            self.ips = new_ips
        return

    ##
    # Thread to initialize a connection
    #
    # @param ip The IP address of the connection
    # @param port The port of the connection
    ##
    def connection_thread(self, ip, port):
        offset = self.file.get_recommendation()
        while offset >= 0:
            request = (self.file_id, offset, self.file.metadata.piece_size)
            connection_thread = self.download_mgr.conn_mgr.get(ip, port)
            connection_thread.request(request)

            self.cv.acquire()
            while not self.should_wake:
                self.cv.wait()
            self.should_wake = False
            self.cv.release()

            offset = self.file.get_recommendation()

        return

    ##
    # Writes data from the file host's response to the file
    #
    # @param json_dict The dictionary of the response
    ##
    def add_data(self, json_dict):
        if json_dict[MessageConstants.FILE] == self.file_id:
            offset = json_dict[MessageConstants.OFFSET]
            data = json_dict[MessageConstants.DATA]
            self.file.write(offset, data)

            self.should_wake = True
            self.cv.notify()
        return