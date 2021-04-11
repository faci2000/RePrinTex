from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

from models.image import Image
from models.image_collection import ImageCollection


class CollectionController:
    def __init__(self, parent, view) -> None:
        self.view = view
        self.parent = parent
        self.collection = ImageCollection(self.parent)

    def get_collection(self)->ImageCollection:
        return self.collection

    def create_collection(self, file_paths):
        self.view.clear()
        self.collection.clear()

        for idx, path in enumerate(file_paths):
            name = path.split('/')[-1]
            image = QImage(path)
            if image.isNull():
                QMessageBox.information(self.parent, "Error", "Cannot load file {}.".format(name))
                return
            pixmap = QPixmap(image)
            image = Image(idx, path, name, pixmap)

            self.collection.add_image(image)
            self.view.add_image_icon(pixmap, name)

    def change_image(self):
        idx = self.view.files_list.currentIndex().row()
        pixmap = self.collection.change_current_image(idx)
        self.parent.image_preview_view.controller.set_new_image(pixmap)
