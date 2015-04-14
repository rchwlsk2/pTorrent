from downloader import Downloader, DownloadConnectionManager
from network_connection import MessageConstants


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
    def __init__(self):
        self.downloaders = {}                               # Key is the file ID
        self.conn_mgr = DownloadConnectionManager(self)
        return

    ##
    # Gets a list of all files that have not been downloaded yet and creates downloaders for them
    ##
    def gather_files(self):
        return

    ##
    # Resumes the downloads of all downloaders
    ##
    def resume_all(self):
        return

    ##
    # Pauses the downloads of all downloaders
    ##
    def pause_all(self):
        return

    ##
    # Sends the response from a file host to a downloader
    #
    # @param json_response The host's response
    ##
    def send_to_downloader(self, json_response):
        file_id = json_response[MessageConstants.FILE]
        downloader = self.downloaders[file_id]
        if downloader is not None:
            downloader.add_data(json_response)
        return