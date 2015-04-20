import os

from client.downloader import Downloader, DownloadConnectionManager
from client.file_manager import MetadataFile
from client.network_connection import MessageConstants
import client.CONSTANTS as CONSTANTS



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
    def __init__(self, root_path):
        self.downloaders = {}                               # Key is the file ID
        self.conn_mgr = DownloadConnectionManager(self)

        self.root_path
        return

    ##
    # Adds a file to the DownloadManager
    ##
    def add_file(self, path):
        metadata = MetadataFile()
        metadata.parse(path)
        filepath = os.path.join(CONSTANTS.ROOT, CONSTANTS.DOWNLOADS, metadata.filename)
        if not os.path.exists(filepath):
            downloader = Downloader(self, path)
            self.downloaders[downloader.file_id] = downloader

        return

    ##
    # Removes a file from the DownloadManager (only to be called when download is finished)
    ##
    def remove_file(self, path):
        metadata = MetadataFile()
        metadata.parse(path)

        del self.downloaders[metadata.file_id]
        return

    ##
    # Resumes the downloads of all Downloaders
    ##
    def resume_all(self):
        for file_id, downloader in self.downloaders.items():
            downloader.start()
        return

    ##
    # Pauses the downloads of all Downloaders
    ##
    def pause_all(self):
        for file_id, downloader in self.downloaders.items():
            downloader.stop()
        return

    ##
    # Sends the response from a file host to a Downloader
    #
    # @param json_response The host's response
    ##
    def send_to_downloader(self, ip, metadata, file_data):
        file_id = metadata[MessageConstants.FILE]
        downloader = self.downloaders[file_id]
        print(self.downloaders, downloader)
        if downloader is not None:
            downloader.add_data(ip, metadata, file_data)
        return