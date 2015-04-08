import math


##
# File that tracks how much of a file was downloaded
#
# @author Paul Rachwalski
# @date Apr 4, 2015
##
class FileMap(object):

    ##
    # Creates a blank file map
    #
    # @param map_file The name of the map file
    # @param size The total size in bytes of the file
    ##
    def __init__(self, map_filename, size, piece_size):
        self.filename = map_filename
        self.map = None
        self.in_progress = []

        self.size = size
        self.bits = int(math.ceil(self.size / piece_size))
        self.bytes = int(math.ceil(self.bits / 8))
        return

    ##
    # Creates an empty bitmap
    #
    # @param piece_size The size of an individual piece of the file
    ##
    def create(self):
        self.map = bytearray(self.bytes)
        return

    ##
    # Loads a file map from disk
    ##
    def load(self):
        with open(self.filename, 'rb') as map_file:
            data = map_file.read()
        self.map = bytearray(data)
        return

    ##
    # Saves the current file map to disk
    ##
    def save(self):
        with open(self.filename, 'wb') as map_file:
            map_file.write(self.map)
        return

    ##
    # Checks that the map is complete and no pieces are missing
    ##
    def is_complete(self):
        if len(self.in_progress) != 0:
            return False

        # Check all but last byte
        if self.bytes > 1:
            for i in range(0, self.bytes - 1):
                if self.map[i] != 255:
                    return False

        # Check last byte
        should_be_set = self.bits % 8
        if should_be_set == 0:
            should_be_set = 8

        expected_val = 255 >> (8 - should_be_set)
        if self.map[self.bytes - 1] != expected_val:
            return False

        return True

    ##
    # Sets a bit to be in progress
    ##
    def set_in_progress(self, bit):
        self.in_progress.append(bit)
        return

    ##
    # Sets a bit in the map
    ##
    def set_complete(self, bit):
        bit_off = int(bit % 8)
        byte_off = int(bit / 8)

        mask = 1 << bit_off
        self.map[byte_off] |= mask


        self.in_progress.remove(bit)
        return

    ##
    # Gives a section of the file to be downloaded
    ##
    def recommend_piece(self):
        for bit in range(0, self.bits):
            bit_off = bit % 8
            byte_off = int(bit / 8)

            # If in progress, ignore
            if bit not in self.in_progress:
                # Otherwise mask and check bit
                section = self.map[byte_off]
                mask = 1 << bit_off
                if not section & mask:
                    return bit

        return -1