import os
import client.CONSTANTS as CONSTANTS
import client.file_manager.FileConstants as FileConstants
from client.file_manager.MetadataFile import MetadataFile


##
# Loads files in downloads folder to ready client
#
# @author Paul Rachwalski
# @date Apr 18, 2015
##
class FileManager(object):

    ##
    # Initializes Download- and UploadManager to pass back to
    #
    # @param down_mgr The DownloadManager instance for the client
    # @param up_mgr The UploadManager instance for the client
    ##
    def __init__(self, down_mgr, up_mgr):
        self.download_mgr = down_mgr
        self.upload_mgr = up_mgr

        self.downloads = []
        self.uploads = []
        return

    ##
    # Picks through all files in Downloads and adds them to the appropriate lists
    ##
    def gather_files(self):
        downloads_path = os.path.join(CONSTANTS.ROOT, CONSTANTS.META_FILES)

        # Get all possible files
        meta_files = []
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
            filepath = os.path.join(CONSTANTS.ROOT, CONSTANTS.DOWNLOADS, metadata.filename)
            if not os.path.exists(filepath):
                self.downloads.append(path)
            else:
                self.uploads.append(path)

        return

    ##
    # Transfers the files to the Download- And UploadManagers themselves
    ##
    def transfer(self):
        for download in self.downloads:
            self.download_mgr.add_file(download)

        for upload in self.uploads:
            self.upload_mgr.add_file(upload)

        return

    ##
    # Clears unnecessary files and adds to UploadManager
    ##
    def finish_downloading(self, download):
        self.downloads.remove(download)
        self.uploads.append(download)

        self.download_mgr.remove_file(download)
        self.upload_mgr.add_file(download)
        return
