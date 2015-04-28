import sys
from PyQt5.QtWidgets import QApplication
from client.pTorrentClient import pTorrentClient
from client.gui.pTorrentWidget import pTorrentWidget


client = None #pTorrentClient()

main_application = QApplication(sys.argv)

client = pTorrentWidget(None)
client.show()

sys.exit(main_application.exec_())
