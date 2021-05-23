import os

from PyQt5.QtWidgets import QFileDialog, QMainWindow

from controllers.controller import Controller
from services.state_saver import write_style_config
from views.archive_creator import ArchiveCreator
from views.guielements.menu.dialogs import Dialogs


class MenuBarController:
    """
    A class handling menu bar actions.

    Attributes
        parent: QMainWindow
        dialogs: Dialogs

    """

    def __init__(self, parent) -> None:
        self.parent: QMainWindow = parent
        self.dialogs: Dialogs = Dialogs(self.parent)

        Controller().set_menubar_controller(self)

    def load_files(self):
        file_paths, _ = QFileDialog.getOpenFileName(self.parent)
        if file_paths:
            Controller().add_image(file_paths)

    def create_archive(self, collection_view):
        create_archive_dialog = ArchiveCreator(collection_view)
        create_archive_dialog.exec_()

    def add_image(self):
        pass

    def remove_images(self):
        Controller().remove_images()

    def remove_collection(self):
        Controller().remove_collection()

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

    def change_style(self, dark):
        if dark:
            write_style_config("dark")
        else:
            write_style_config("light")
            self.parent.view_menu.light.setChecked(True)
            self.parent.view_menu.dark.setChecked(False)
        self.dialogs.open_style()
