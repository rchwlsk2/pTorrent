from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QObject


class Communicate(QObject):
    callback = pyqtSignal()

##
# A clickable play/pause image!
#
# @author Paul Rachwalski
# @date Apr 27, 2015
##
class PlayButtonWidget(QLabel):

    PLAY = "resources/play_button.png"
    PAUSE = "resources/pause_button.png"

    ##
    # Sets image parameter to be the pixel map
    ##
    def __init__(self, parent=None):
        super(PlayButtonWidget, self).__init__(parent)

        pixel_map = QPixmap(self.PLAY)
        self.setPixmap(pixel_map)
        self.connectNotify(self, )

        return

    def set_callback(self, callback):
        self.signal = Communicate()
        selfd
        return


    def mouseReleaseEvent(self, ev):
        self.emit(pyqtSignal('clicked()'))
        return