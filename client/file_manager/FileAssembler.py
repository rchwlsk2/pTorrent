import os
import binascii

from client.file_manager.FileMap import FileMap
from client.file_manager.MetadataFile import MetadataFile
from client.file_manager.FileConstants import *
import client.CONSTANTS as CONSTANTS



##
# Manages the assembly of a file from it's pieces
#
# @author Paul Rachwalski
# @date Apr 5, 2015
##
class FileAssembler(object):

    ##
    # Initializes the file assembler
    #
    # @param metadata_file The file path to the metadata file
    ##
    def __init__(self, metadata_file):
        print(CONSTANTS.ROOT, metadata_file)
        self.metadata = MetadataFile()
        self.metadata = self.metadata.parse(metadata_file)

        self.filename = self.metadata.filename + "." + TEMP_EXT
        self.file_path = CONSTANTS.ROOT + CONSTANTS.DOWNLOADS + self.filename

        map_name = CONSTANTS.ROOT + CONSTANTS.MAPS + self.metadata.file_id + "." + MAP_EXT
        self.map = FileMap(map_name, self.metadata.size, self.metadata.piece_size)

        # Initialize map file and empty file
        if not os.path.exists(self.file_path):
            self.map.create()
            self.map.save()
            self.create_empty_file()
        else:
            self.map.load()
        return

    ##
    # Creates new empty file
    #
    # @return The path to the empty file
    ##
    def create_empty_file(self):
        # Create empty file of designated size
        with open(self.file_path, "wb") as file:
            file.seek(self.metadata.size - 1)
            file.write(b"\x00")
        return

    ##
    # Gets the byte offset of the the recommended piece in the file
    #
    # @return The byte offset if there are pieces left, or -1 otherwise
    ##
    def get_recommendation(self):
        recommended_bit = self.map.recommend_piece()

        # Mark in progress
        self.map.set_in_progress(recommended_bit)

        if recommended_bit >= 0:
            return recommended_bit * self.metadata.piece_size
        return -1

    ##
    # Gets whether the download is complete or not
    #
    # @return The boolean indicating download completion
    ##
    def is_downloaded(self):
        return self.map.is_complete()

    ##
    # Renames a file with the proper extension so it can be opened with the appropriate program
    ##
    def convert_to_full(self):
        if self.is_downloaded():
            new_name = CONSTANTS.ROOT + CONSTANTS.DOWNLOADS + self.metadata.filename
            os.rename(self.file_path, new_name)
            self.file_path = new_name
        return

    ##
    # Writes section to file
    #
    # @param data The data to write to the file
    ##
    def write(self, offset, data):
        with open(self.file_path, "rb+") as file:
            file.seek(offset)
            file.write(data)

        # Mark complete
        self.map.set_complete(offset / self.metadata.piece_size)
        self.map.save()
        return
