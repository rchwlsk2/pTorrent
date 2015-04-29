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
        self.progress_size = QLabel("0 kB")

        main_layout.addWidget(self.download_name, 5)
        main_layout.addWidget(self.progress_size, 1)

        self.setLayout(main_layout)
        return

    ##
    # Updates the progress values
    #
    # @param percent Float value of percent downloaded
    # @param size Float value of file size downloaded
    ##
    def set_progress(self, size):
        new_size = str(size) + " kB"
        self.progress_size.setText(new_size)
        return