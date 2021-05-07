from typing import List
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

from models.image import Image
from models.image_collection import ImageCollection


class CollectionController:
    def __init__(self, parent, view) -> None:
        self.view = view
        self.parent = parent
        self.active_collection=None
        self.collections:List[ImageCollection] = []   #ImageCollection(self.parent)

    def get_collection(self) -> ImageCollection:
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

    def add_collection(self,path):
        self.collections.append(ImageCollection(self.parent,path))
        self.active_collection=len(self.collections)-1
        for img in self.collections[self.active_collection-1].collection:
            self.view.add_image_icon(img.pixmap, img.name)
        print("changing image to: "+self.collections[self.active_collection].collection[0].name)
        self.change_image(self.collections[self.active_collection].collection[0])

    def change_image(self,img=None):
        if img is None:
            idx = self.view.files_list.currentIndex().row()
            picture = self.collections[self.active_collection].change_current_image(idx)
            self.parent.image_preview_view.controller.set_new_image(picture)
        else:
            self.parent.image_preview_view.controller.set_new_image(img)


