from PyQt5.QtWidgets import *


##
# Item in the download list
#
# @author Paul Rachwalski
# @date Apr 27, 2015
##
class DownloadListItemWidget(QWidget):

    PAUSE_LABEL = "Pause"
    RESUME_LABEL = "Resume"

    ##
    # Initializes a DownloadListItemWidget for a file with name
    ##
    def __init__(self, name, parent=None):
        super(DownloadListItemWidget, self).__init__(parent)

        self.name = name
        self.downloader = None
        self.downloading = False
        main_layout = QHBoxLayout()

        self.download_name = QLabel(name)
        self.progress_percent = QLabel("0%")
        self.progress_size = QLabel("0 kB")
        self.pause_button = QPushButton(self.RESUME_LABEL)

        main_layout.addWidget(self.download_name, 3)
        main_layout.addWidget(self.progress_percent, 1)
        main_layout.addWidget(self.progress_size, 1)
        main_layout.addWidget(self.pause_button, 1)

        self.pause_button.clicked.connect(self.on_click)
        self.setLayout(main_layout)
        return

    ##
    # Sets the downloader
    ##
    def set_downloader(self, downloader):
        self.downloader = downloader
        return

    ##
    # Function that is run when button is clicked
    ##
    def on_click(self):
        if self.pause_button.text() == self.PAUSE_LABEL:
            self.pause_button.setText(self.RESUME_LABEL)
        else:
            self.pause_button.setText(self.PAUSE_LABEL)

        if self.downloader:
            if not self.downloading:
                self.downloading = True
                self.downloader.start()
            elif self.downloading:
                self.downloading = False
                self.downloader.stop()

        return

    ##
    # Updates the progress values
    #
    # @param percent Float value of percent downloaded
    # @param size Float value of file size downloaded
    ##
    def set_progress(self, percent, size):
        new_percent = "%3.2f" % percent
        new_percent += "%"
        self.progress_percent.setText(new_percent)

        new_size = "%10f" % size
        new_size += " kB"
        self.progress_size.setText(new_size)
        return