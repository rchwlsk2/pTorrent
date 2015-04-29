import sys, os
from client import pTorrentClient


##
# pTorrent Client Terminal program
#
# @author Paul Rachwalski
# @date Apr 21, 2015
##
class ptTerm(object):

    def __init__(self):
        print("\n--------------------\n pTorrent P2P Client \n--------------------\n")
        print("Setup")
        port = int(input("Upload port: "))
        tracker_ip = input("Tracker IP: ")
        tracker_port = int(input("Tracker port: "))

        self.should_run = True

        self.ptorrent = pTorrentClient("client", "localhost", port, tracker_ip, tracker_port)
        self.ptorrent.start()

        return

    def main_menu(self):
        while self.should_run:
            print("\n--------------------\n Menu \n--------------------")
            print("(1) View download status")
            print("(2) Add download")
            print("(3) Add upload")
            print("(4) Pause download")
            print("(5) Exit")
            print("--------------------")

            inp = input("> ")
            if inp == "1":
                self.download_status()
            elif inp == "2":
                self.add_download()
            elif inp == "3":
                self.add_upload()
            elif inp == "4":
                self.pause_download()
            elif inp == "5":
                self.ptorrent.exit()
                self.should_run = False

        return

    def download_status(self):
        while True:
            os.system("clear")
            print("Downloads")
            print("---------")
            for dwnldr in self.ptorrent.download_mgr.downloaders.keys():
                progress =  "{:3.1f}%".format(self.ptorrent.download_mgr.downloaders[dwnldr].file.map.get_progress()*100)
                print(progress + " " + dwnldr)
            print("---------\n")
        return

    def add_download(self):
        return

    def add_upload(self):
        return

    def pause_download(self):
        return


if __name__ == "__main__":
    term = ptTerm()