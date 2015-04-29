import os
import shutil

from client.downloader import DownloadManager
from client.uploader import UploadManager
from client.file_manager import FileUtils, MetadataFile
import client.CONSTANTS as CONSTANTS


##
# The main client application class
#
# @author Paul Rachwalski
# @date Apr 20, 2015
##
class pTorrentClient(object):

    ##
    # Initializes objects for uploading and downloading
    #
    # @param root The root path of the project
    # @param port The port to bind the uploader to
    # @param tracker_ip The IP address of the tracker server
    # @param tracker_port The port of the tracker server
    ##
    def __init__(self, root, ip, port, tracker_ip, tracker_port):
        self.root = root
        self.download_mgr = DownloadManager(root, self.download_done_callback)
        self.upload_mgr = UploadManager(root, ip, port, tracker_ip, tracker_port)

        self.downloads, self.uploads = FileUtils.gather_files(root)
        for meta in self.downloads:
            self.download_mgr.register_file(meta)
        for meta in self.uploads:
            self.upload_mgr.register_file(meta)

        return

    ##
    # Allows the upload manager and download manager to begin
    ##
    def start(self):
        self.download_mgr.resume_all()
        self.upload_mgr.resume_all()

        return

    ##
    # Gracefully ends all uploads and downloads to cause the least amount of data loss
    ##
    def exit(self):
        self.download_mgr.pause_all()
        self.upload_mgr.stop()
        return

    ##
    # Adds a file for upload
    ##
    def add_upload_file(self, file_path):
        piece = 2 ** 15
        tracker = "54.200.76.207:6045"

        file = file_path.split("/")[-1]
        new_file = os.path.join(self.root, CONSTANTS.DOWNLOADS, file)
        shutil.copy(file_path, new_file)

        metadata = MetadataFile()
        meta_path = metadata.generate(new_file, tracker, piece_size=piece)

        self.uploads.append(meta_path)
        self.upload_mgr.register_file(meta_path)
        return

    ##
    # Adds a download if the metadata file already exists
    ##
    def add_download_metadata(self, meta_path):
        file = meta_path.split("/")[-1]
        new_meta = os.path.join(self.root, CONSTANTS.META_FILES, file)
        shutil.copy(meta_path, new_meta)

        self.downloads.append(new_meta)
        self.download_mgr.register_file(new_meta)
        return

    def delete_all_data(self, meta_path):
        return

    ##
    # Callback function to move downloaded files from the download module to upload module
    #
    # @param file_id The ID of the file
    # @param metadata_path The path to the metadata file of the complete download
    ##
    def download_done_callback(self, file_id, metadata_path):
        self.download_mgr.deregister_file(file_id)
        self.downloads.remove(metadata_path)

        self.uploads.append(metadata_path)
        self.upload_mgr.register_file(metadata_path)
        return
