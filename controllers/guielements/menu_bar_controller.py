from views.archive_creator import ArchiveCreator
from PyQt5.QtWidgets import QFileDialog


class MenuBarController:
    def __init__(self, parent) -> None:
        self.parent = parent

    def load_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self.parent)
        if file_paths:
            self.parent.collection_view.controller.create_collection(file_paths)

    def create_archive(self,collection_view):
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
