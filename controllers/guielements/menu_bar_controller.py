from PyQt5.QtWidgets import QFileDialog
import os
from services.images_provider import ImagesProvider
from views.archive_creator import ArchiveCreator
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

    def remove_image(self):
        pass

    def remove_collection(self):
        pass

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

    def change_style(self, dark):
        if dark:
            f = open("dark", "w+")
            f.close()
            self.parent.view_menu.dark.setChecked(True)
            self.parent.view_menu.light.setChecked(False)
        else:
            if os.path.isfile("dark"):
                os.remove("dark")
            self.parent.view_menu.light.setChecked(True)
            self.parent.view_menu.dark.setChecked(False)
        self.dialogs.open_style()
