import unittest
from uploader import UploadManager
from file_manager import MetadataFile
import CONSTANTS


##
# Test the downloader class's functionality
#
# @author Paul Rachwalski
# @date Apr 10, 2015
##
class TestUpload(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        garb_meta = MetadataFile()
        garb_meta.generate("downloads/garb.txt", "localhost", piece_size=32768)

        up_mgr = UploadManager("", '', CONSTANTS.PORT)
        return