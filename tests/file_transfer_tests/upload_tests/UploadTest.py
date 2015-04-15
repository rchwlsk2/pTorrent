import unittest
from uploader import UploadManager
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
        up_mgr = UploadManager("", '', CONSTANTS.PORT)
        return