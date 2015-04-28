from PyQt5.QtWidgets import *
import sys
from client.gui.DownloadListItemWidget import DownloadListItemWidget
from client.gui.UploadListItemWidget import UploadListItemWidget


##
# Main GUI widget for the pTorrent client
#
# @author Paul Rachwalski
# @date Apr 27, 2015
##
class pTorrentWidget(QWidget):

    SAMPLES = (("image.png", 14.43, 10002),
               ("fish.mp9", 81.3223, 122.44))

    PAUSE_ALL_LABEL = "Pause All"
    RESUME_ALL_LABEL = "Resume All"

    ##
    # Creates the application GUI
    #
    # @param client The pTorrentClient instance
    ##
    def __init__(self, client, Parent=None):
        super(pTorrentWidget, self).__init__(Parent)

        self.downloads = []
        self.uploads = []

        self.loaders_layout = QHBoxLayout()

        self.loaders_layout.addLayout(self.create_download_layout())
        self.loaders_layout.addLayout(self.create_upload_widget())

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.loaders_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("pTorrent Client")
        self.showMaximized()

    ##
    # Creates the horizontal layout with relevant buttons to downloads
    ##
    def create_download_buttons(self):
        button_layout = QHBoxLayout()

        pause_all_button = QPushButton(self.PAUSE_ALL_LABEL)
        add_download_button = QPushButton("Add Download")
        pause_all_button.setFixedWidth(140)
        add_download_button.setFixedWidth(140)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout.addWidget(spacer, 3)
        button_layout.addWidget(pause_all_button, 1)
        button_layout.addWidget(add_download_button, 1)
        return button_layout

    ##
    # Creates layout for downloading half of client
    ##
    def create_download_layout(self):
        download_buttons = self.create_download_buttons()
        download_list = QListWidget(self)

        download_labels = QHBoxLayout()
        download_label = QLabel("Downloads")
        progress_label = QLabel("Progress (%)")
        size_label = QLabel("Current Size")
        pause_label = QLabel("Pause/Resume")
        download_labels.addWidget(download_label, 3)
        download_labels.addWidget(progress_label, 1)
        download_labels.addWidget(size_label, 1)
        download_labels.addWidget(pause_label, 1)

        for name, percent, size in self.SAMPLES:
            download_list_item = DownloadListItemWidget(name)
            download_list_item.set_progress(percent, size)

            list_widget = QListWidgetItem(download_list)
            list_widget.setSizeHint(download_list_item.sizeHint())

            download_list.addItem(list_widget)
            download_list.setItemWidget(list_widget, download_list_item)

        download_layout = QVBoxLayout()
        download_layout.addLayout(download_buttons, 1)
        download_layout.addLayout(download_labels, 1)
        download_layout.addWidget(download_list, 20)
        return download_layout

    ##
    # Creates the horizontal layout with relevant buttons to uploads
    ##
    def create_upload_buttons(self):
        button_layout = QHBoxLayout()

        pause_all_button = QPushButton(self.PAUSE_ALL_LABEL)
        add_upload_button = QPushButton("Add Upload")
        pause_all_button.setFixedWidth(140)
        add_upload_button.setFixedWidth(140)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout.addWidget(spacer, 3)
        button_layout.addWidget(pause_all_button, 1)
        button_layout.addWidget(add_upload_button, 1)
        return button_layout

    ##
    # Creates layout for uploading half of client
    ##
    def create_upload_widget(self):
        upload_buttons = self.create_upload_buttons()

        upload_labels = QHBoxLayout()
        upload_label = QLabel("Uploads")
        amount_label = QLabel("Amount")
        upload_labels.addWidget(upload_label, 5)
        upload_labels.addWidget(amount_label, 1)

        upload_list = QListWidget(self)

        for name, percent, size in self.SAMPLES:
            upload_list_item = UploadListItemWidget(name)
            upload_list_item.set_progress(size)

            list_widget = QListWidgetItem(upload_list)
            list_widget.setSizeHint(upload_list_item.sizeHint())

            upload_list.addItem(list_widget)
            upload_list.setItemWidget(list_widget, upload_list_item)

        upload_layout = QVBoxLayout()
        upload_layout.addLayout(upload_buttons, 2)
        upload_layout.addLayout(upload_labels, 1)
        upload_layout.addWidget(upload_list, 20)
        return upload_layout

    ##
    # Refreshes the values in the uploader/downloader lists
    ##
    def refresh_lists(self):
        return
