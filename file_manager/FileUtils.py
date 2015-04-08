import os
import zipfile

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