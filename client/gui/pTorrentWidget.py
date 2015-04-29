from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import threading
from time import sleep
from client.gui.DownloadListItemWidget import DownloadListItemWidget
from client.gui.UploadListItemWidget import UploadListItemWidget
from client.downloader.Downloader import Downloader
from client.file_manager.FileConstants import *
from client.file_manager.MetadataFile import MetadataFile


##
# Communication object to be able to send signals to main UI thread
##
class GuiCommunication(QObject):
    add_download = pyqtSignal(str, float, float, Downloader)
    add_upload = pyqtSignal(str)

##
# Main GUI widget for the pTorrent client
#
# @author Paul Rachwalski
# @date Apr 27, 2015
##
class pTorrentWidget(QWidget):

    PAUSE_LABEL = "Pause"
    RESUME_LABEL = "Resume"

    PAUSE_ALL_LABEL = "Pause All"
    RESUME_ALL_LABEL = "Resume All"

    ##
    # Creates the application GUI
    #
    # @param client The pTorrentClient instance
    ##
    def __init__(self, client, Parent=None):
        super(pTorrentWidget, self).__init__(Parent)

        self.client = client
        self.bridge = GuiCommunication()
        self.bridge.add_download.connect(self.add_download_item)
        self.bridge.add_upload.connect(self.add_upload_item)

        self.downloads = {}
        self.uploads = {}
        self.download_widgets = {}
        self.upload_widgets = {}
        self.download_list = None
        self.upload_list = None

        self.downloading_state = False
        self.uploading_state = False

        self.loaders_layout = QHBoxLayout()

        self.loaders_layout.addLayout(self.create_download_layout(), 2)
        self.loaders_layout.addLayout(self.create_upload_widget(), 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.loaders_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("pTorrent Client")

        self.refresh_lists()
        self.refresh_progress()
        return

    ##
    # Creates the horizontal layout with relevant buttons to downloads
    #
    # @return The layout containing the buttons for the download half
    ##
    def create_download_buttons(self):
        button_layout = QHBoxLayout()

        self.pause_all_down_button = QPushButton(self.RESUME_ALL_LABEL)
        add_download_button = QPushButton("Add Download")
        self.pause_all_down_button.setFixedWidth(140)
        add_download_button.setFixedWidth(140)

        self.pause_all_down_button.clicked.connect(self.download_all)
        add_download_button.clicked.connect(self.new_download)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout.addWidget(spacer, 3)
        button_layout.addWidget(self.pause_all_down_button, 1)
        button_layout.addWidget(add_download_button, 1)
        return button_layout

    ##
    # Creates layout for downloading half of client
    #
    # @return The layout containing the download half of the GUI
    ##
    def create_download_layout(self):
        download_buttons = self.create_download_buttons()
        self.download_list = QListWidget(self)

        download_labels = QHBoxLayout()

        download_label = QLabel("Downloads")
        progress_label = QLabel("Progress (%)")
        size_label = QLabel("Current Size")
        pause_label = QLabel("Pause/Resume")

        download_labels.addWidget(download_label, 3)
        download_labels.addWidget(progress_label, 1)
        download_labels.addWidget(size_label, 1)
        download_labels.addWidget(pause_label, 1)

        download_layout = QVBoxLayout()
        download_layout.addLayout(download_buttons, 1)
        download_layout.addLayout(download_labels, 1)
        download_layout.addWidget(self.download_list, 20)
        return download_layout

    ##
    # Creates the horizontal layout with relevant buttons to uploads
    #
    # @return The layout containing all of the buttons for the upload half
    ##
    def create_upload_buttons(self):
        button_layout = QHBoxLayout()

        self.pause_all_up_button = QPushButton(self.RESUME_ALL_LABEL)
        add_upload_button = QPushButton("Add Upload")
        self.pause_all_up_button.setFixedWidth(140)
        add_upload_button.setFixedWidth(140)

        self.pause_all_up_button.clicked.connect(self.upload_all)
        add_upload_button.clicked.connect(self.new_upload)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout.addWidget(spacer, 3)
        button_layout.addWidget(self.pause_all_up_button, 1)
        button_layout.addWidget(add_upload_button, 1)
        return button_layout

    ##
    # Creates layout for uploading half of client
    #
    # @return The layout containing the upload half of the GUI
    ##
    def create_upload_widget(self):
        upload_buttons = self.create_upload_buttons()

        upload_labels = QHBoxLayout()
        upload_label = QLabel("Uploads")
        upload_labels.addWidget(upload_label, 1)

        self.upload_list = QListWidget(self)

        upload_layout = QVBoxLayout()
        upload_layout.addLayout(upload_buttons, 2)
        upload_layout.addLayout(upload_labels, 1)
        upload_layout.addWidget(self.upload_list, 20)
        return upload_layout

    ##
    # GUI function to add an item to the download list
    #
    # @param name The name of the file
    # @param progress The progress percentage of the download
    # @param size The amount of the file downloaded so far
    # @downloader The downloader associated with the file
    ##
    def add_download_item(self, name, progress, size, downloader):
        download_list_item = DownloadListItemWidget(name)
        download_list_item.set_progress(progress * 100, size)
        download_list_item.set_downloader(downloader)

        list_widget = QListWidgetItem(self.download_list)
        list_widget.setSizeHint(download_list_item.sizeHint())

        self.download_list.itemDoubleClicked.connect(self.delete_download_item)
        self.download_list.addItem(list_widget)
        self.download_list.setItemWidget(list_widget, download_list_item)
        self.download_widgets[name] = (download_list_item, list_widget)

        self.download_list.update()
        return

    ##
    # GUI function to add an item to the upload list
    #
    # @param name The name of the file
    ##
    def add_upload_item(self, name):
        upload_list_item = UploadListItemWidget(name)

        list_widget = QListWidgetItem(self.upload_list)
        list_widget.setSizeHint(upload_list_item.sizeHint())

        self.upload_list.itemDoubleClicked.connect(self.delete_upload_item)
        self.upload_list.addItem(list_widget)
        self.upload_list.setItemWidget(list_widget, upload_list_item)
        self.upload_widgets[name] = upload_list_item

        if name in self.download_widgets.keys():
            widgets = self.download_widgets[name]
            self.download_list.takeItem(self.download_list.row(widgets[1]))

            del self.download_widgets[name]
            del self.downloads[name]

        self.upload_list.update()
        self.download_list.update()
        return

    ##
    # Deletes an item and the associated files
    ##
    def delete_download_item(self, item):
        widget = self.download_list.itemWidget(item)
        if widget:
            if widget.downloading:
                widget.on_click()

            name = self.download_list.itemWidget(item).name

            if name in self.download_widgets.keys():
                del self.download_widgets[name]
                del self.downloads[name]
                self.download_list.takeItem(self.download_list.row(item))

                for meta in self.client.downloads:
                    if name in meta:
                        metadata = MetadataFile()
                        metadata.parse(meta)
                        self.client.download_mgr.deregister_file(metadata.file_id)
                        if self.client.download_mgr.downloaders[metadata.file_id]:
                            file_path = self.client.download_mgr.downloaders[metadata.file_id].file.file_path
                            map_path = self.client.download_mgr.downloaders[metadata.file_id].file.map.path
                            os.remove(map_path)
                            os.remove(file_path)

                        os.remove(meta)
                        break

        self.download_list.update()
        return

    ##
    # Deletes an item and the associated files
    ##
    def delete_upload_item(self, item):
        widget = self.upload_list.itemWidget(item)
        if widget:
            name = self.upload_list.itemWidget(item).name

            if name in self.upload_widgets.keys():
                del self.upload_widgets[name]
                del self.uploads[name]
                self.upload_list.takeItem(self.upload_list.row(item))

                for meta in self.client.uploads:
                    if name in meta:
                        metadata = MetadataFile()
                        metadata.parse(meta)
                        self.client.upload_mgr.deregister_file(metadata.file_id)
                        os.remove(meta)
                        break

        self.upload_list.update()
        return

    ##
    # Adds a new metadata file for downloading
    ##
    def new_download(self):
        meta, val = QFileDialog.getOpenFileName(self, 'New Download', '~')

        if meta.split(".")[-1] == METADATA_EXT:
            self.client.add_download_metadata(meta)
        return

    ##
    # Adds a new file for uploading
    ##
    def new_upload(self):
        file_path, val = QFileDialog.getOpenFileName(self, 'New Upload', '~')

        self.client.add_upload_file(file_path)
        return

    ##
    # Refreshes the uploader/downloader lists every 1 second
    ##
    def refresh_lists(self):
        next_iteration_timer = threading.Timer(1, self.refresh_lists)
        next_iteration_timer.start()

        downloaders = self.client.download_mgr.downloaders
        for key in downloaders.keys():
            downloader = downloaders[key]
            filemap = downloader.file.map
            meta = downloader.file.metadata

            name = meta.filename
            progress = filemap.get_progress()
            size = meta.size * progress
            downloading = True

            if name not in self.download_widgets.keys():
                self.bridge.add_download.emit(name, progress, size, downloader)
            else:
                self.download_widgets[name][0].set_progress(progress * 100, size)

            self.downloads[name] = (name, progress, size, downloading, downloader)

        uploaders = self.client.upload_mgr.files
        for key in uploaders.keys():
            path, meta = uploaders[key]

            if meta.filename not in self.uploads.keys():
                self.bridge.add_upload.emit(meta.filename)

            self.uploads[meta.filename] = (meta.filename, 0)

        return

    ##
    # Refreshes the progress values in the uploader/downloader lists every 1/10 second
    ##
    def refresh_progress(self):
        next_iteration_timer = threading.Timer(0.1, self.refresh_progress)
        next_iteration_timer.start()

        downloaders = self.client.download_mgr.downloaders
        for key in downloaders.keys():
            downloader = downloaders[key]
            map = downloader.file.map
            meta = downloader.file.metadata

            name = meta.filename
            progress = map.get_progress()
            size = meta.size * progress
            downloading = True

            self.downloads[name] = (name, progress, size, downloading)
            if name in self.download_widgets.keys():
                self.download_widgets[name][0].set_progress(progress * 100, size)

        return

    ##
    # Handler function to pause/resume downloads
    ##
    def download_all(self):
        if self.downloading_state:
            self.pause_all_down_button.setText(self.PAUSE_ALL_LABEL)
            self.downloading_state = False

            for widgets in self.download_widgets.items():
                widgets[0].downloading = False
                widgets[0].pause_button.setText(self.PAUSE_LABEL)

            self.client.download_mgr.pause_all()

        else:
            self.pause_all_down_button.setText(self.RESUME_ALL_LABEL)
            self.downloading_state = True

            for key in self.download_widgets.keys():
                widgets = self.download_widgets[key]
                widgets[0].downloading = True
                widgets[0].pause_button.setText(self.RESUME_LABEL)

            self.client.download_mgr.resume_all()

        self.download_list.update()
        return

    ##
    # Handler function to pause/resume uploads
    ##
    def upload_all(self):
        if self.uploading_state:
            self.uploading_state = False
            self.pause_all_up_button.setText(self.RESUME_ALL_LABEL)
            self.client.upload_mgr.pause_all()
        else:
            self.uploading_state = True
            self.pause_all_up_button.setText(self.PAUSE_ALL_LABEL)
            self.client.upload_mgr.resume_all()
        return

