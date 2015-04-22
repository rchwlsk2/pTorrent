import unittest

from client.uploader import UploadManager
from client.file_manager import FileUtils
import client.CONSTANTS as CONSTANTS



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
        up_mgr = UploadManager("", 10010, "54.200.76.207", 6045)

        downloads, uploads = FileUtils.gather_files("")
        for meta in uploads:
            up_mgr.register_file(meta)

        up_mgr.resume_all()
        return