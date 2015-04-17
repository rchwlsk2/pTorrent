import unittest
import os
import filecmp

from client.file_manager.FileAssembler import FileAssembler



##
# Manages the assembly of a file from it's pieces
#
# @author Paul Rachwalski
# @date Apr 5, 2015
##
class TestFileAssembler(unittest.TestCase):

    METADATA_FILE = "tests/file_manager_tests/data/a.txt-2048-262144.ptorrent"

    def setUp(self):
        pass

    ##
    # Test that the proper values are initialized
    ##
    def test_constructor(self):
        assembler = FileAssembler(self.METADATA_FILE)

        self.assertEqual(assembler.metadata.filename, "a.txt", "Incorrect metadata filename")
        self.assertEqual(assembler.metadata.size, 2048, "Incorrect metadata file size")
        self.assertEqual(assembler.metadata.piece_size, 64, "Incorrect metadata piece size")

        self.assertTrue(os.path.exists(assembler.file_path), "Created blank file does not exist")
        self.assertTrue(os.path.exists(assembler.map.filename), "Created map does not exist")

        os.remove(assembler.file_path)
        os.remove(assembler.map.filename)
        return

    ##
    # Test that the recommendation function returns the proper byte offset
    ##
    def test_recommendation(self):
        assembler = FileAssembler(self.METADATA_FILE)

        self.assertEqual(assembler.get_recommendation(), 0, "Incorrect initial recommendation")

        assembler.map.set_complete(0)
        assembler.map.set_in_progress(1)
        assembler.map.set_complete(1)
        assembler.map.set_in_progress(2)
        self.assertEqual(assembler.get_recommendation(), 3 * assembler.metadata.piece_size,
                         "Incorrect  partial recommendation")

        os.remove(assembler.file_path)
        os.remove(assembler.map.filename)
        return

    ##
    # Test completion and file renaming at end of download
    ##
    def test_conversion(self):
        assembler = FileAssembler(self.METADATA_FILE)

        self.assertTrue(os.path.exists(assembler.file_path), "Created blank file does not exist")
        for i in range(0, assembler.map.bits):
            assembler.map.set_in_progress(i)
            assembler.map.set_complete(i)

        assembler.convert_to_full()
        self.assertTrue(os.path.exists(assembler.file_path), "Created full file does not exist")

        os.remove(assembler.file_path)
        os.remove(assembler.map.filename)
        return

    ##
    # Test that segments are properly written to a file
    ##
    def test_write(self):
        sample = bytes("hellomanhellomanhellomanhellomanhellomanhellomanhellomanhelloman", "UTF-8")
        assembler = FileAssembler(self.METADATA_FILE)

        self.assertTrue(os.path.exists(assembler.file_path), "Created blank file does not exist")
        assembler.map.set_in_progress(0)
        assembler.write(0, sample)

        with open(assembler.file_path, "rb") as file:
            file.seek(0)
            data_read = file.read(assembler.metadata.piece_size)

        self.assertEqual(data_read, sample, "Incorrect bytes loaded from file")

        os.remove(assembler.file_path)
        os.remove(assembler.map.filename)
        return

    ##
    # Test a sample file creation
    ##
    def test_all(self):
        path = "tests/file_manager_tests/data/a.txt"
        assembler = FileAssembler(self.METADATA_FILE)
        self.assertTrue(os.path.exists(assembler.file_path), "Created blank file does not exist")

        with open(path, "rb") as file:
            while not assembler.is_downloaded():
                offset = assembler.get_recommendation()

                file.seek(offset)
                data = file.read(assembler.metadata.piece_size)
                assembler.write(offset, data)
        assembler.convert_to_full()

        self.assertTrue(os.path.exists(assembler.file_path), "Created blank file does not exist")
        self.assertTrue(filecmp.cmp(path, assembler.file_path), "Incorrect file comparison")

        os.remove(assembler.file_path)
        os.remove(assembler.map.filename)
        return