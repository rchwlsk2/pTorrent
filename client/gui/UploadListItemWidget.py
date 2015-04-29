from PyQt5.QtWidgets import *


##
# Item in the download list
#
# @author Paul Rachwalski
# @date Apr 27, 2015
##
class UploadListItemWidget(QWidget):

    PAUSE_LABEL = "Pause"
    RESUME_LABEL = "Resume"

    ##
    # Initializes a DownloadListItemWidget for a file with name
    ##
    def __init__(self, name, parent=None):
        super(UploadListItemWidget, self).__init__(parent)

        self.name = name
        main_layout = QHBoxLayout()

        self.download_name = QLabel(name)

        main_layout.addWidget(self.download_name)

        self.setLayout(main_layout)
        return