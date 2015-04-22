import threading
import json
import signal
import os
import sys
from socket import *
from socket import error as sock_err

from client.uploader.TrackerThread import TrackerThread
from client.network_connection import ServerConnection
from client.file_manager import MetadataFile, FileConstants
import client.CONSTANTS as CONSTANTS


##
# Manages all file uploads
#
# @author Paul Rachwalski
# @date Apr 14, 2015
##
from client.network_connection import MessageConstants


class UploadManager(object):

    ##
    # Initializes dictionary of files and connections and starts accepting server connections
    ##
    def __init__(self, root_path, port, tracker_ip, tracker_port):
        self.upload_ip = CONSTANTS.LOCALHOST
        self.upload_port = port

        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port

        self.files = {}             # Key is the file ID
        self.connections = {}       # Key is the IP

        # Exit handler
        signal.signal(signal.SIGINT, self.exit_handler)

        # Initialize tracker connection thread
        self.tracker_conn = TrackerThread(tracker_ip, tracker_port)
        self.tracker_conn.start()

        self.gather_files(root_path)

        temp_upload_ip = self.upload_ip
        if temp_upload_ip == CONSTANTS.LOCALHOST:
            temp_upload_ip = ""
        address = (temp_upload_ip, self.upload_port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        print("Starting uploads... ")
        try:
            self.sock.bind(address)
        except sock_err as e:
            print('Socket bind for uploader failed. Error Code: ' + str(e))
            sys.exit()

        hostname = tracker_ip if tracker_ip != '' else "localhost"
        print("Upload server is running at " + hostname + ":" + str(tracker_port) + "\n")
        self.sock.listen(10)

        # Start the server loop
        self.server_loop()

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
    def register_file(self, file_id, path):
        self.tracker_conn.add(file_id, self.upload_ip, self.upload_port)
        self.files[file_id] = path
        return

    ##
    # Gets a list of all files that have been downloaded and creates uploaders for them
    ##
    def gather_files(self, root_path):
        downloads_path = os.path.join(root_path, CONSTANTS.META_FILES)

        # Get all possible files
        meta_files = []
        print(os.listdir(downloads_path))
        for file in os.listdir(downloads_path):
            filepath = os.path.join(downloads_path, file)
            is_file = os.path.isfile(filepath)
            is_meta = file.endswith(FileConstants.METADATA_EXT)
            if is_file and is_meta:
                meta_files.append(filepath)

        # Create appropriate downloaders if the file is not downloaded
        for path in meta_files:
            metadata = MetadataFile()
            metadata.parse(path)
            filepath = os.path.join(root_path, CONSTANTS.DOWNLOADS, metadata.filename)
            if os.path.exists(filepath):
                print(filepath)
                #uploader = Uploader(self, path, self.tracker_ip, self.tracker_port)
                #self.files[metadata.file_id] = filepath
                self.register_file(metadata.file_id, filepath)

        return

    ##
    # Continuously accepts connections from downloaders looking for a fix
    ##
    def server_loop(self):
        while True:
            connection, address = self.sock.accept()
            print('Connected with ' + address[0] + ':' + str(address[1]))

            UploadConnectionThread(self, connection).start()
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
        return

    ##
    # Overrides the default run function to uploads parts of files
    ##
    def run(self):
        print("UPLOAD THREAD")
        connection = ServerConnection(self.connection)

        while True:
            # Read entire request
            request = ""
            #part = None
            #while part != "":
            #    part = self.connection.recv(CONSTANTS.BUFFER_SIZE).decode()
            #    request += part
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
                    connection.send_response(file, file_id, offset, length)

        connection.terminate()
        return