import unittest
import socket
from file_manager import MetadataFile
from downloader import Downloader
from tracker import TrackerConstants


##
# Test the downloader class's functionality
#
# @author Paul Rachwalski
# @date Apr 10, 2015
##
class TestDownloader(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        file = "data/a.txt"
        meta = "data/a.txt-2048-262144.ptorrent"

        meta_file = MetadataFile()
        meta_file.parse(meta)

        add_request = TrackerConstants.ADD + meta_file.file_id + " localhost"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect(('', 6044))
        sock.send(add_request.encode())

        downloader = Downloader(meta, '', 6044)
        downloader.start()

        return