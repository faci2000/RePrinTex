from PyQt5.QtWidgets import QFileDialog


class MenuBarController:
    def __init__(self, parent) -> None:
        self.parent = parent

    def load_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self.parent)
        if file_paths:
            self.parent.collection_view.controller.create_collection(file_paths)

    def save_image(self):
        pass

    def save_image_as(self):
        pass

    def save_all_images(self):
        pass
