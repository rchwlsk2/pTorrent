import sys
from PyQt5.QtWidgets import QApplication
from client.pTorrentClient import pTorrentClient
from client.gui.pTorrentWidget import pTorrentWidget
from client.CONSTANTS import *


client = pTorrentClient("client", LOCALHOST, 9999, "54.200.76.207", 6045)

main_application = QApplication(sys.argv)
main_application.aboutToQuit.connect(sys.exit)

client = pTorrentWidget(client)
client.show()

sys.exit(main_application.exec_())
