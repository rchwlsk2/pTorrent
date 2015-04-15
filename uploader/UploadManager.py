import os
import threading

from uploader.Uploader import Uploader
from file_manager import MetadataFile, FileConstants
import CONSTANTS


##
# Manages all file uploads
#
# @author Paul Rachwalski
# @date Apr 14, 2015
##
class UploadManager(object):

    ##
    # Initializes dictionary of downloaders and a DCM
    ##
    def __init__(self, root_path, tracker_ip, tracker_port):
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port

        self.uploaders = {}         # Key is the file ID
        self.connections = {}       # Key is the IP

        self.gather_files(root_path)
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
                uploader = Uploader(self, path, self.tracker_ip, self.tracker_port)
                self.uploaders[uploader.file_id] = uploader

        return

    ##
    # Continuously accepts connections from downloaders looking for a fix
    ##
    def server_loop(self):
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