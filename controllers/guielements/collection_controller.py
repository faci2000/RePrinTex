from typing import List
import os
import json

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

import models.image_collection as mic
import views.guielements.docks.collection_view as vgdcv
from controllers.controller import Controller
from models.image import Image
from services.images_provider import ImagesProvider, EmptyCollectionsListException
from services.state_reader import read_saved_collections, read_collections_json


class CollectionController:
    def __init__(self, parent, view) -> None:
        from services.images_provider import ImagesProvider
        self.view: vgdcv.CollectionView = view
        self.parent = parent
        self.active_collection = None
        self.image_provider = ImagesProvider()
        self.image_provider.image_selector = self
        self.collections: List[mic.ImageCollection] = []  # ImageCollection(self.parent)
        Controller().set_collection_controller(self)

    def get_collection(self) -> mic.ImageCollection:
        return self.image_provider.get_current_collection()

    def add_images(self, file_path):
        collection = self.image_provider.get_current_collection()
        print(file_path)
        new_img = Image(len(collection.collection),file_path,file_path.split('/')[-1].split('.')[0],QPixmap(QImage(file_path)))
        collection.add_image(new_img)
        self.view.add_image_icon(new_img.last_org_pixmap , new_img.name)

    def change_collection(self, index: int = None, text: str = None):

        print(index, text)
        if index:
            coll = self.image_provider.change_current_collection(new_collection_index=index)
        elif text:
            coll = self.image_provider.change_current_collection(new_collection_text=text)
        else:
            return
        self.view.collections_list.setCurrentText(coll.name)
        self.fill_collection_list_view(coll)
        if len(coll.collection) > 0:
            self.image_provider.change_current_image(0)
            self.image_provider.set_image_to_display()
        else:
            self.image_provider.image_view.view.label_modified.clear()
            self.image_provider.image_view.view.label_original.clear()

    def fill_collection_list_view(self, collection: mic.ImageCollection):
        self.view.clear()

        for img in collection.collection:
            image = QImage(img.path)
            if image.isNull():
                QMessageBox.information(self.parent, "Error", "Cannot load file {}.".format(img.name))
                return
            pixmap = QPixmap(image)
            self.view.add_image_icon(pixmap, img.name)
        self.active_collection = collection

    def add_collection(self, path: str, name: str):
        new_col = mic.ImageCollection(parent=self.parent, path=path, name=name)
        changed_collection = self.image_provider.add_new_collection(new_col)
        print(changed_collection)
        self.fill_name_combobox()
        print("filled")
        if not changed_collection:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle("Change current collection")
            msg.setText("Do you want to change current collection to recently added?")
            msg.setInformativeText("All changes made to currently edited collections will be saved.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.buttonClicked.connect(lambda button: (msg.standardButton(
                button) == QMessageBox.Yes) and self.image_provider.image_selector.change_collection(text=new_col.name))
            msg.buttonClicked.connect(lambda button: print(msg.standardButton(button) == QMessageBox.Yes))
            msg.exec()
        # for img in new_col.collection:
        #     self.view.add_image_icon(convert_cv2Image_to_QPixmap(cv2.imread(img.path)), img.name)
        # self.change_image(self.collections[self.active_collection].collection[0])
        # self.image_provider.set_image_to_display()

    def fill_name_combobox(self):
        self.view.collections_list.clear()
        for coll in self.image_provider.collections:
            self.view.collections_list.addItem(coll.name)

    def change_image(self, img=None):
        if img is None:
            idx = self.view.files_list.currentIndex().row()
            picture = self.image_provider.change_current_image(idx)
            self.image_provider.set_image_to_display()
        else:
            Controller().set_new_image(img)

    def remove_images(self):
        try:
            to_remove = self.view.files_list.selectedItems()
            if len(to_remove) == 0:
                raise Exception("No images selected!")

            coll = ImagesProvider().get_current_collection()

            for item in to_remove:
                idx = self.view.files_list.indexFromItem(item).row()
                del coll.collection[idx]
                self.view.files_list.takeItem(idx)
            self.view.files_list.update()

        except (Exception, EmptyCollectionsListException) as e:
            Controller().communicator.error.emit(str(e))
            return

    def remove_collection(self):
        idx = self.view.collections_list.currentIndex()
        coll_json = read_collections_json()

        if self.active_collection:
            name = self.active_collection.name
            for coll in ImagesProvider().collections:
                if name == coll.name:
                    ImagesProvider().collections.remove(coll)
                    ImagesProvider().current_collection_index = None
                    self.active_collection = None
                    break
            for coll in coll_json:
                if coll["name"] == name:
                    path = "./data/colldet/" + coll["path"]
                    if os.path.exists(path):
                        os.remove(path)
                    break
            with open('config.json') as json_file:
                data = json.load(json_file)
                for coll in data['collections']:
                    if coll['name'] == name:
                        data['collections'].remove(coll)
                        break
                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
        self.view.collections_list.removeItem(idx)

        if len(self.image_provider.collections) > 0:
            self.change_collection(self.view.collections_list.currentText())
        else:
            self.image_provider.image_view.view.label_modified.clear()
            self.image_provider.image_view.view.label_original.clear()
            self.view.collections_list.clear()
            self.view.files_list.clear()

