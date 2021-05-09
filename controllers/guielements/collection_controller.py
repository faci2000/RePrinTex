from imgmaneng.img_converter import convert_cv2Image_to_QPixmap
import cv2
import models.image_collection as mic
import views.guielements.docks.collection_view as vgdcv
from typing import List
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

from models.image import Image


class CollectionController:
    def __init__(self, parent, view) -> None:
        from services.images_provider import ImagesProvider
        self.view:vgdcv.CollectionView = view
        self.parent = parent
        self.active_collection=None
        self.image_provider = ImagesProvider()
        self.image_provider.image_selector = self
        self.collections:List[mic.ImageCollection] = []   #ImageCollection(self.parent)

    def get_collection(self) -> mic.ImageCollection:
        return self.image_provider.get_current_collection()

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

    def change_collection(self, index:int):
        coll = self.image_provider.change_current_collection(index)
        self.fill_collection_list_view(coll)
        if len(coll.collection)>0:
            self.image_provider.change_current_image(0)

    def fill_collection_list_view(self,collection:mic.ImageCollection):
        self.view.clear()

        for img in collection.collection:
            image = QImage(img.path)
            if image.isNull():
                QMessageBox.information(self.parent, "Error", "Cannot load file {}.".format(img.name))
                return
            pixmap = QPixmap(image)
            self.view.add_image_icon(pixmap, img.name)

    def add_collection(self,path:str,name:str):
        changed_collection = self.image_provider.add_new_collection(mic.ImageCollection(parent=self.parent,path=path,name=name))
        if(not changed_collection):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle("Change current collection")
            msg.setText("Do you want to change current collection to recently added?")
            msg.setInformativeText("All changes made to currently edited collections will be saved.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.buttonClicked.connect(lambda button: (button==QMessageBox.Yes) and self.image_provider.change_current_collection_to_added_recently())

        for img in self.image_provider.get_recently_added_collection().collection:
            self.view.add_image_icon(convert_cv2Image_to_QPixmap(cv2.imread(img.path)), img.name)
        # self.change_image(self.collections[self.active_collection].collection[0])
        self.image_provider.set_image_to_display()

    def fill_name_combobox(self):
        for coll in self.image_provider.collections:
            self.view.collections_list.addItem(coll.name)

    def change_image(self,img=None):
        if img==None:
            idx = self.view.files_list.currentIndex().row()
            picture = self.image_provider.change_current_image(idx)
            self.image_provider.set_image_to_display()
        else:
            self.parent.image_preview_view.controller.set_new_image(img)


