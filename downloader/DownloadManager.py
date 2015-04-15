import os

from downloader import Downloader, DownloadConnectionManager
from network_connection import MessageConstants
from file_manager import MetadataFile, FileConstants
import CONSTANTS


##
# Manages all currently downloading files
#
# @author Paul Rachwalski
# @date Apr 14, 2015
##
class DownloadManager(object):

    ##
    # Initializes dictionary of downloaders and a DCM
    ##
    def __init__(self, root_path, tracker_ip, tracker_port):
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port

        self.downloaders = {}                               # Key is the file ID
        self.conn_mgr = DownloadConnectionManager(self)

        self.gather_files(root_path)
        return

    ##
    # Gets a list of all files that have not been downloaded yet and creates downloaders for them
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
            if not os.path.exists(filepath):
                print(filepath)
                downloader = Downloader(self, path, self.tracker_ip, self.tracker_port)
                self.downloaders[downloader.file_id] = downloader

        return

    ##
    # Resumes the downloads of all downloaders
    ##
    def resume_all(self):
        for file_id, downloader in self.downloaders.items():
            downloader.start()
        return

    ##
    # Pauses the downloads of all downloaders
    ##
    def pause_all(self):
        for file_id, downloader in self.downloaders.items():
            downloader.stop()
        return

    ##
    # Sends the response from a file host to a downloader
    #
    # @param json_response The host's response
    ##
    def send_to_downloader(self, ip, json_response):
        file_id = json_response[MessageConstants.FILE]
        downloader = self.downloaders[file_id]
        if downloader is not None:
            downloader.add_data(ip, json_response)
        return