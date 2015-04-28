import unittest

from client.file_manager import FileUtils
from client.downloader import DownloadManager


##
# Test the downloader class's functionality
#
# @author Paul Rachwalski
# @date Apr 10, 2015
##
class TestDownload(unittest.TestCase):

    def setUp(self):
        pass

    def done_callback(self, a, b):
        return

    def test_something(self):
        down_mgr = DownloadManager("client", self.done_callback)
        print(down_mgr.conn_mgr.connections)

        downloads, uploads = FileUtils.gather_files("client")
        for meta in downloads:
            down_mgr.register_file(meta)

        down_mgr.resume_all()
        return