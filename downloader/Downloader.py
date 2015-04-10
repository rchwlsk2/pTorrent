import threading
import socket
from file_manager import FileAssembler
from tracker import TrackerConstants
from network_connection import ClientConnection


##
# In charge of downloading a file from all available hosts
#
# @author Paul Rachwalski
# @date Apr 9, 2015
##
class Downloader(object):

    SLEEP_TIME = 3
    BUF_SIZE = 1024
    PORT = 46969

    ##
    # Starts the download threads and the thread to keep the ip list up to date
    #
    # @param metadata The path to the metadata file
    ##
    def __init__(self, metadata, ip, port):
        self.file = FileAssembler(metadata)
        self.host = ip
        self.port = port

        self.ip_threads = []
        self.ips = []

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
    # Thread to periodically refresh the list of IP addresses to download from
    ##
    def ip_refresh(self):
        if self.should_run:
            # Restart timer
            threading.Timer(self.SLEEP_TIME, self.ip_refresh).start()

            # Send request to server
            message = TrackerConstants.GET + self.file.metadata.file_id
            print(message)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((self.host, self.port))

            new_ips = []
            response = sock.recv(self.BUF_SIZE).decode()
            if response == TrackerConstants.CONNECT_SUCCESS:
                sock.send(message.encode())
                ip_str = sock.recv(self.BUF_SIZE).decode()
                new_ips = ip_str.split(" ")

            # Setup connection to tracker
            for ip in new_ips:
                if ip not in self.ips:
                    thread = ConnectionThread(ip, self.port, target=self.connection_thread, args=(ip, self.port))
                    self.ip_threads.append(thread)
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
    ##
    def connection_thread(self, ip, port):
        client_conn = ClientConnection(ip, port)

        offset = self.file.get_recommendation()
        while offset >= 0:
            data = client_conn.sock.recv(self.file.metadata.piece_size)
            if not data: break

            data = data.decode()
            self.file.write(offset, data)

            offset = self.file.get_recommendation()

        client_conn.terminate()
        return


##
# Simple extension of Thread class to be able to store the associated IP and port with the connection
##
class ConnectionThread(threading.Thread):

    ##
    # Extends default constructor to store the ip and port of the file host
    #
    # @param ip The IP address of the host
    # @param port The port
    def __init__(self, ip, port, group=None, target=None, name=None, args=(), kwargs={}):
        super.__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)

        self.ip = ip
        self.port = port
        return