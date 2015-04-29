import threading
import json
import signal
import os
import sys
from socket import *
from socket import error as sock_err
from time import sleep

from client.uploader.TrackerThread import TrackerThread
from client.network_connection import ServerConnection
from client.file_manager import MetadataFile
from client.network_connection import MessageConstants
import client.CONSTANTS as CONSTANTS


##
# Manages all file uploads
#
# @author Paul Rachwalski
# @date Apr 14, 2015
##
class UploadManager(object):

    ##
    # Initializes dictionary of files and connections and starts accepting server connections
    ##
    def __init__(self, root_path, ip, port, tracker_ip, tracker_port):
        self.root_path = root_path
        self.upload_ip = ip
        self.upload_port = port

        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port

        self.should_run = True
        self.files = {}             # Key is the file ID
        self.threads = []           # Connection threads

        # Exit handler
        signal.signal(signal.SIGINT, self.exit_handler)

        # Initialize tracker connection thread
        self.tracker_conn = TrackerThread(tracker_ip, tracker_port)
        self.tracker_conn.start()

        temp_upload_ip = self.upload_ip
        if temp_upload_ip == CONSTANTS.LOCALHOST:
            temp_upload_ip = ""
        address = (temp_upload_ip, self.upload_port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        try:
            self.sock.bind(address)
        except sock_err as e:
            print('Socket bind for uploader failed. Error Code: ' + str(e))
            sys.exit()

        print("Upload server is running at " + ip + ":" + str(port) + "\n")
        self.sock.listen(10)

        return

    ##
    # Pauses the uploading
    ##
    def pause_all(self):
        for thread in self.threads:
            thread.pause()
        return

    ##
    # Starts the uploading
    ##
    def resume_all(self):
        threading.Thread(target=self.server_loop).start()
        for thread in self.threads:
            thread.resume()
        return

    ##
    # Ends all threads
    ##
    def stop(self):
        self.should_run = False
        sleep(0.1)
        for thread in self.threads:
            thread.stop()
            thread.join()
        return

    ##
    # Exit SIGINT handler (ctrl+c)
    ##
    def exit_handler(self, signum, frame):
        print("\nUploads stopped!")
        self.tracker_conn.remove_all(self.upload_ip)

        self.sock.close()
        self.tracker_conn.stop()
        sys.exit(0)
        return

    ##
    # Registers a given file with the tracker
    ##
    def register_file(self, path):
        print("Adding... ", path)
        metadata = MetadataFile()
        metadata.parse(path)
        if metadata.file_id not in self.files.keys():
            filepath = os.path.join(self.root_path, CONSTANTS.DOWNLOADS, metadata.filename)
            if os.path.exists(filepath):
                add_result = self.tracker_conn.add(metadata.file_id, self.upload_ip, self.upload_port)
                self.files[metadata.file_id] = (filepath, metadata)
        return

    def deregister_file(self, file_id):
        if file_id in self.files.keys():
            del self.files[file_id]
        return

    ##
    # Continuously accepts connections from downloaders looking for a fix
    ##
    def server_loop(self):
        while self.should_run:
            connection, address = self.sock.accept()
            print("Accepted connection!")
            connection_thread = UploadConnectionThread(self, connection)
            self.threads.append(connection_thread)
            connection_thread.start()
        return


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
    def __init__(self, upload_mgr, connection):
        super().__init__(group=None, target=None, name=None, args=(), kwargs={})

        self.upload_mgr = upload_mgr
        self.connection = connection

        self.should_run = True
        self.should_upload = True
        self.upload_cv = threading.Condition()
        return

    ##
    # Halts upload
    ##
    def pause(self):
        if self.should_upload:
            self.should_upload = False
        return

    ##
    # Resumes an upload
    ##
    def resume(self):
        self.should_upload = True
        with self.upload_cv:
            self.upload_cv.notify()
        return

    ##
    # Stops the thread's execution
    ##
    def stop(self):
        self.resume()
        self.should_run = False
        return

    ##
    # Overrides the default run function to uploads parts of files
    ##
    def run(self):
        connection = ServerConnection(self.connection)

        while self.should_run:
            # Pause the upload if necessary
            while not self.should_upload:
                self.upload_cv.wait()

            request = self.connection.recv(CONSTANTS.BUFFER_SIZE).decode()

            # Check that request is proper
            if request is not "":
                request_dict = json.loads(request)
                print("Received request", request_dict)

                file_id = request_dict[MessageConstants.FILE]
                offset = request_dict[MessageConstants.OFFSET]
                length = request_dict[MessageConstants.SIZE]

                if file_id in self.upload_mgr.files:
                    file = self.upload_mgr.files[file_id]
                    connection.send_response(file[0], file_id, offset, length)

        connection.terminate()
        return