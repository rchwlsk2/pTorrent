from file_manager import FileAssembler


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
    # @param metadata The path to the metadata file
    ##
    def __init__(self, metadata):
        self.ips = []
        self.file = FileAssembler(metadata)

        return

    ##
    # Starts the download
    ##
    def start(self):
        return

    ##
    # Stops the download and saves the progress
    ##
    def stop(self):
        return

    ##
    # Thread to periodically refresh the list of IP addresses to download from
    ##
    def ip_refresh_thread(self):
        return

    ##
    # Thread to initialize a connection
    ##
    def connection_thread(self):
        return