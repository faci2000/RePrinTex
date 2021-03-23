from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

from models.image import Image


class ImageCollection:
    def __init__(self, parent):
        self.parent = parent
        self.collection = []
        self.current_image_id = None

    def add_image(self, image):
        self.collection.append(image)

    def clear(self):
        self.current_image_id = None
        self.collection = []

    # ta nazwa mi sie totalne nie podoba ale chodzi o pixmape i nazwe do collection_view zeby pokazać miniaturke
    def get_image_elements(self, idx):
        return self.collection[idx].pixmap, self.collection[idx].name

    def change_current_image(self, idx):
        self.current_image_id = idx
        return self.collection[idx].pixmap

    def get_current_pixmap(self):
        return self.collection[self.current_image_id].pixmap
