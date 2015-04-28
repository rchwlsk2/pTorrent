import threading
import socket
import os

from client.file_manager import FileAssembler
from tracker.TrackerConstants import *
from client.network_connection import MessageConstants
import client.CONSTANTS as CONSTANTS


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
    def __init__(self, download_mgr, metadata, done_callback):
        self.download_mgr = download_mgr
        self.metadata_path = metadata
        self.done_callback = done_callback

        self.file = FileAssembler(metadata)
        self.file_lock = threading.Lock()

        self.file_id = self.file.metadata.file_id
        tracker = self.file.metadata.tracker.split(":")
        self.tracker_ip = tracker[0]
        self.tracker_port = int(tracker[1])

        self.ip_threads = {}
        self.ips = []

        self.should_run = True
        return

    ##
    # Starts the download
    ##
    def start(self):
        self.should_run = True
        threading.Thread(target=self.ip_refresh).start()

        for ip in self.ip_threads.keys():
            thread = self.ip_threads[ip]
            if thread.isAlive():
                thread.wake()
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
        if self.should_run:
            new_ips = []
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Restart timer
            threading.Timer(CONSTANTS.UPDATE_INTERVAL, self.ip_refresh).start()

            # Send request to server
            message = TrackerConstants.GET + self.file_id
            print(message)

            sock.connect((self.tracker_ip, self.tracker_port))
            response = sock.recv(CONSTANTS.BUFFER_SIZE).decode()
            if response == TrackerConstants.CONNECT_SUCCESS:
                sock.send(message.encode())
                ip_str = sock.recv(CONSTANTS.BUFFER_SIZE).decode()
                if ip_str == "get failed":
                    return
                new_ips = ip_str.split("-")

            # Setup connection to tracker
            for ip in new_ips:
                if ip not in self.ips:
                    split_ip = ip.split(":")
                    thread = DownloaderThread(self, split_ip[0], int(split_ip[1]))
                    self.ip_threads[ip] = thread
                    self.download_mgr.conn_mgr.add(split_ip[0], int(split_ip[1]))
                    thread.start()

            to_delete = []
            for file_id in self.ip_threads.keys():
                cur_thread = self.ip_threads[file_id]
                if cur_thread.ip not in new_ips:
                    cur_thread.join()
                    to_delete.append(file_id)

            for file_id in to_delete:
                del self.ip_threads[file_id]

            self.ips = new_ips
            sock.close()
        return

    ##
    # Writes data from the file host's response to the file
    #
    # @param json_dict The dictionary of the response
    ##
    def add_data(self, ip, metadata, file_data):
        if metadata[MessageConstants.FILE] == self.file_id:
            offset = metadata[MessageConstants.OFFSET]

            with self.file_lock:
                self.file.write(offset, file_data)
                print("File written to, progress: {:3.1f}%".format(self.file.map.get_progress()*100))
                if self.file.is_downloaded():
                    self.should_run = False

                    self.file.convert_to_full()
                    os.remove(self.file.map.filename)
                    self.done_callback(self.file_id, self.metadata_path)
                    return

            if self.should_run and ip in self.ip_threads.keys():
                thread = self.ip_threads[ip]
                if thread.isAlive():
                    thread.wake()
        return


##
# Custom thread class to manage the downloading of a file from a particular host
##
class DownloaderThread(threading.Thread):

    ##
    # Initializes the thread
    #
    # @param downloader The downloader that has created the thread
    # @param ip The IP address of the file host
    # @param port The port of the file host
    ##
    def __init__(self, downloader, ip, port):
        super().__init__(group=None, target=None, name=None, args=(), kwargs={})

        self.downloader = downloader
        self.ip = ip
        self.port = port

        # Prevent queueing an entire file immediately
        self.should_wake = False
        self.cv = threading.Condition()

        return

    ##
    # Wakes the thread to continue running
    ##
    def wake(self):
        self.should_wake = True
        with self.cv:
            self.cv.notify()
        return

    ##
    # Overrides the default run method for a thread to
    ##
    def run(self):
        with self.downloader.file_lock:
            offset = self.downloader.file.get_recommendation()

        while offset >= 0:
            file_id = self.downloader.file_id
            piece_size = self.downloader.file.metadata.piece_size
            file_request = (file_id, offset, piece_size)

            download_mgr = self.downloader.download_mgr
            connection_thread = download_mgr.conn_mgr.get(self.ip, self.port)
            connection_thread.request(file_request)

            with self.cv:
                while not self.should_wake:
                    self.cv.wait()
                self.should_wake = False

            with self.downloader.file_lock:
                offset = self.downloader.file.get_recommendation()

        return