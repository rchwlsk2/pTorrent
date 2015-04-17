import json
import os

from client.file_manager.FileConstants import *
import client.CONSTANTS as CONSTANTS


##
# Manages creation and interpretation of .ptorrent files
#
# @author Paul Rachwalski
# @date Apr 3, 2015
##
class MetadataFile(object):

    ##
    # Initializes metadata variables
    ##
    def __init__(self):
        self.tracker = None
        self.filename = None
        self.file_id = None
        self.size = 0
        self.piece_size = 0

        return

    ##
    # Creates a metadata file for the given file
    #
    # @param filename The path to the file
    # @return The path to the metadata file
    ##
    def generate(self, filename, tracker, piece_size=262144):
        if not os.path.isfile(filename):
            return None

        self.tracker = tracker
        self.filename = filename.split("/")[-1]
        self.size = os.path.getsize(filename)
        self.piece_size = piece_size

        # File ID consists of the filename, size, and piece size separated by dashes
        self.file_id = self.filename + "-" + str(self.size) + "-" + str(self.piece_size)

        metadata = {TRACKER: self.tracker,
                    FILE_ID: self.file_id,
                    FILE_NAME: self.filename,
                    FILE_SIZE: self.size,
                    FILE_PIECE_SIZE: self.piece_size}
        json_str = json.dumps(metadata, indent=4)

        meta_filename = CONSTANTS.ROOT + CONSTANTS.META_FILES + self.file_id + "." + METADATA_EXT

        with open(meta_filename, 'w') as meta_file:
            meta_file.write(json_str)

        return meta_filename

    ##
    # Loads all relavant information from a given metadata file
    #
    # @param metadata_file The path to the metadata file
    # @return The current metadata file object
    ##
    def parse(self, metadata_file):
        good_ext = metadata_file.split(".")[-1] == METADATA_EXT
        good_file = os.path.isfile(metadata_file)
        if not good_ext or not good_file:
            return None

        with open(metadata_file, 'r') as json_file:
            metadata = json.load(json_file)

        self.tracker = metadata[TRACKER]
        self.file_id = metadata[FILE_ID]
        self.filename = metadata[FILE_NAME]
        self.size = metadata[FILE_SIZE]
        self.piece_size = metadata[FILE_PIECE_SIZE]

        return self

