from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

from threads.worker_decorator import multi_thread_runner
from views.archive_creator import ArchiveCreator
from PyQt5.QtWidgets import QFileDialog, QDialog, QGridLayout

from views.guielements.menu.dialogs import Dialogs


class MenuBarController:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.dialogs = Dialogs(self.parent)

    def load_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self.parent)
        if file_paths:
            self.parent.collection_view.controller.create_collection(file_paths)

    def create_archive(self, collection_view):
        create_archive_dialog = ArchiveCreator(collection_view)
        create_archive_dialog.exec_()
    
    def save_image(self):
        pass

    def export_all_images(self):
        pass

    def export_image_as(self):
        pass

    def export_image(self):
        pass

    def export_all_as(self):
        pass

    def clean_page(self):
        self.dialogs.open_clean()

    def increase_contrast(self):
        self.dialogs.open_contrast()

    def remove_stains(self):
        self.dialogs.open_stains()
