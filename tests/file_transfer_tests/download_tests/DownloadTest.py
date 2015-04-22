import unittest
import socket
from time import sleep

from client.file_manager import MetadataFile
from client.downloader import DownloadManager
from tracker import TrackerConstants


##
# Test the downloader class's functionality
#
# @author Paul Rachwalski
# @date Apr 10, 2015
##
class TestDownload(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        down_mgr = DownloadManager("client")
        print(down_mgr.conn_mgr.connections)
        down_mgr.resume_all()

        return