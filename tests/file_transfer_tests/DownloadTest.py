import unittest
import socket
from time import sleep

from file_manager import MetadataFile
from downloader import Downloader, DownloadManager
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
        ameta = "tmp/meta/a.txt-2048-262144.ptorrent"
        bmeta = "tmp/meta/b.txt-2048-262144.ptorrent"

        ameta_file = MetadataFile()
        ameta_file.parse(ameta)
        bmeta_file = MetadataFile()
        bmeta_file.parse(bmeta)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect(('', 6045))

        a_add_request = TrackerConstants.ADD + ameta_file.file_id + " localhost"
        #sock.sendall(a_add_request.encode())

        sleep(0.1)

        b_add_request = TrackerConstants.ADD + bmeta_file.file_id + " localhost"
        #sock.sendall(b_add_request.encode())


        #downloader = Downloader(meta, '', 6045)
        #downloader.start()

        down_mgr = DownloadManager("", '', 6045)
        print(down_mgr.conn_mgr.connections)
        down_mgr.resume_all()

        return