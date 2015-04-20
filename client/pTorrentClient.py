import multiprocessing
from client.application import UploadProcess, DownloadProcess


##
# The client application
#
# @author Paul Rachwalski
# @date Apr 20, 2015
##
class pTorrentClient(object):

    ##
    # Starts the initial processes for uploading and downloading
    def __init__(self):
        self.download_process = None
        self.upload_process = None

        return

    def start_processes(self):
        return

    def exit(self):
        return

    def gather_files(self):
        return