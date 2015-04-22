import os
import zipfile

import client.CONSTANTS as CONSTANTS
from client.file_manager.FileConstants import *
from client.file_manager.MetadataFile import MetadataFile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED


##
# Utilities common to the file management of the pTorrent client
#
# @author Paul Rachwalski
# @date Apr 1, 2015
##
class FileUtils(object):

    modes = {zipfile.ZIP_DEFLATED: 'deflated',
             zipfile.ZIP_STORED: 'stored'}

    def __init__(self):
        pass

    ##
    # Compresses a file or folder to a zip file
    #
    # @param source_path The path to the file or folder to compress
    # @param out_path The path the to compressed file outputted
    ##
    @staticmethod
    def compress_file(source_path, out_path):
        zip = zipfile.ZipFile(out_path, mode='w')

        try:
            if os.path.isdir(source_path):
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        zip.write(os.path.join(root, file))
            else:
                zip.write(source_path)

        finally:
            zip.close()

        return

    ##
    # Decompresses a zip file
    #
    # @param source_path The path to the zip file
    # @param out_dir The path to the output directory
    ##
    @staticmethod
    def decompress_file(source_path, out_dir):
        with zipfile.ZipFile(source_path) as zf:
            '''for member in zf.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                words = member.filename.split('/')
                path = out_dir

                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''):
                        continue
                    path = os.path.join(path, word)

                zf.extract(member, path)'''
            zf.extractall(out_dir)
        return

    ##
    # Creates a checksum of a file to compare against a remote file
    #
    # @param file_path The file to create the checksum for
    ##
    @staticmethod
    def create_checksum(file_path):
        return

    ##
    # Picks through all files in Downloads and adds them to the appropriate lists
    #
    # @param downloads_path The path to the downloads folder
    # @return A pair of lists where the first is download files and the second is upload files
    ##
    @staticmethod
    def gather_files(root_path):
        meta_path = os.path.join(root_path, CONSTANTS.META_FILES)
        downloads_path = os.path.join(root_path, CONSTANTS.DOWNLOADS)

        downloads = []
        uploads = []

        # Get all possible files
        meta_files = []
        for file in os.listdir(meta_path):
            file_path = os.path.join(meta_path, file)

            is_file = os.path.isfile(file_path)
            is_meta = file.endswith(METADATA_EXT)
            if is_file and is_meta:
                meta_files.append(file_path)

        # Place files in appropriate list
        for path in meta_files:
            metadata = MetadataFile()
            metadata.parse(path)
            file_path = os.path.join(downloads_path, metadata.filename)
            if not os.path.exists(file_path):
                downloads.append(path)
            else:
                uploads.append(path)

        return downloads, uploads