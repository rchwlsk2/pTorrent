import unittest
import os

from client.file_manager import MetadataFile



##
# Tests MetadataFile creation and loading
#
# @author Paul Rachwalski
# @date Apr 5, 2015
##
class TestMetadataFile(unittest.TestCase):

    def setUp(self):
        pass

    ##
    # Tests that the default constructor initializes the proper empty values
    ##
    def test_empty_constructor(self):
        metadata = MetadataFile()

        self.assertIsNone(metadata.tracker, "Metadata tracker has value")
        self.assertIsNone(metadata.filename, "Metadata file name has value")
        self.assertIsNone(metadata.file_id, "Metadata file ID has value")
        self.assertEqual(metadata.size, 0, "Metadata size has value")
        self.assertEqual(metadata.piece_size, 0, "Metadata piece size has value")

        return

    ##
    # Tests that a simple file can be generated and parsed back into the class
    ##
    def test_generate_parse_a(self):
        filename = "tests/file_manager_tests/data/a.txt"
        tracker = "123.456.789.0"

        metadata = MetadataFile()
        out_file = metadata.generate(filename, tracker)

        loaddata = MetadataFile()
        loaddata.parse(out_file)

        self.assertEqual(loaddata.tracker, tracker, "Incorrect tracker loaded")
        self.assertEqual(loaddata.filename, "a.txt", "Incorrect file name loaded")
        self.assertEqual(loaddata.file_id, metadata.file_id, "Incorrect file id loaded")
        self.assertEqual(loaddata.size, metadata.size, "Incorrect size loaded")
        self.assertEqual(loaddata.piece_size, metadata.piece_size, "Incorrect piece size loaded")

        os.remove(out_file)
        return

    ##
    # Tests that a different simple file can be generated and parsed back into the class
    ##
    def test_generate_parse_b(self):
        filename = "tests/file_manager_tests/data/dir/b.txt"
        tracker = "123.456.789.5"

        metadata = MetadataFile()
        out_file = metadata.generate(filename, tracker)

        loaddata = MetadataFile()
        loaddata.parse(out_file)

        self.assertEqual(loaddata.tracker, tracker, "Incorrect tracker loaded")
        self.assertEqual(loaddata.filename, "b.txt", "Incorrect file name loaded")
        self.assertEqual(loaddata.file_id, metadata.file_id, "Incorrect file id loaded")
        self.assertEqual(loaddata.size, metadata.size, "Incorrect size loaded")
        self.assertEqual(loaddata.piece_size, metadata.piece_size, "Incorrect piece size loaded")

        os.remove(out_file)
        return