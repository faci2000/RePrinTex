import traceback
import controllers.guielements.collection_controller as cgcc
from PyQt5.QtGui import QPixmap
from imgmaneng.img_converter import convert_cv2Image_to_QPixmap
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from imgmaneng.lines_streightening import lines_streigtening
from imgmaneng.img_cleaner import clean_page, increase_contrast, remove_stains
import cv2
import models.effects as me
from controllers.guielements.image_preview_controller import ImagePreviewController
from models.image import Image
from typing import Any, List, Set
import models.image_collection as mic
from threading import Lock
import numpy as np


class ImagesProviderMeta(type):
    _instances={}

    _lock: Lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args,**kwargs)
                self._instances[self] = instance
        return self._instances[self]

class EmptyCollectionsListException(Exception):
    pass

class EmptyCollectionException(Exception):
    pass

class ImagesProvider(metaclass=ImagesProviderMeta):
    def __init__(self,image_view:ImagePreviewController=None) -> None:
        import controllers.guielements.collection_controller as cgcc
        self.collections:List[mic.ImageCollection] = []
        self.current_collection_index:int = None
        self.current_image_index:int = None
        self.image_view:ImagePreviewController = image_view
        self.image_selector:cgcc.CollectionController = None

    def load_data(self):
        import services.state_reader as ssr
        self.collections = ssr.read_saved_collections()
        print(self.collections)
        ssr.read_view_config(self)
        try:
            self.image_selector.fill_name_combobox()
            self.image_selector.view.collections_list.setCurrentIndex(self.current_collection_index)
            self.set_image_to_display()
        except Exception:
            traceback.print_exc()

    def get_recently_added_collection(self)->mic.ImageCollection:
        if len(self.collections)==0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[len(self.collections)-1]

    def get_current_collection(self)->mic.ImageCollection:
        if len(self.collections)==0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[self.current_collection_index]

    def get_current_collection_effects(self)->me.Effects:
        return self.get_current_collection().effects

    def get_current_collection_org_lines(self)->Set:
        return self.get_current_collection().lines_on_org

    def get_current_image(self)->Image:
        collection = self.get_current_collection()
        if len(collection.collection)==0:
            raise EmptyCollectionException("Image collection is empty. Add some images to collection first.")
        else:
            return collection.collection[self.current_image_index]

    def change_current_image(self,new_image_index:int)->Image:
        old_index = self.current_image_index
        try:
            self.current_image_index = new_image_index
            return self.get_current_image()
        except IndexError:
            print("Index out of bounds.")
            self.current_image_index = old_index
            return self.get_current_image()

    def change_current_collection(self, new_collection_index:int)->mic.ImageCollection:
        old_index = self.current_collection_index
        try:
            self.current_collection_index = new_collection_index
            return self.get_current_collection()
        except:
            print("Index out of bounds.")
            self.current_collection_index = old_index
            return self.get_current_collection()

    def add_new_collection(self,new_image_collection:mic.ImageCollection)->bool: # return true if changed current collection
        self.collections.append(new_image_collection)                        # otherwise return false 
        if self.current_collection_index == None:
            self.current_collection_index = len(self.collections)-1
            self.image_selector.view.collections_list.setCurrentIndex(self.current_collection_index)
            if len(new_image_collection.collection)>0:
                self.current_image_index = 0
            return True
        else:
            return False
    def add_new_image(self,image:Image)->bool:
        self.get_current_collection().add_image(Image)
        self.change_current_image(len(self.get_current_collection().collection)-1)
        self.set_image_to_display()

    def change_current_collection_to_added_recently(self)->None:
        self.current_collection_index = len(self.collections)-1
        self.image_selector.view.collections_list.setCurrentIndex(self.current_collection_index)
        if len(self.get_current_collection())==0:
            self.current_image_index=None
        else:
            self.current_image_index=0

    def set_image_to_display(self):
        image = cv2.imread(self.get_current_image().path)
        self.get_current_image().last_org_pixmap = convert_cv2Image_to_QPixmap(image)
        print(self.get_current_image())
        print(self.get_current_image().last_org_pixmap)
        print("set pixmap mod")
        self.get_current_image().last_mod_pixmap = convert_cv2Image_to_QPixmap(image)
        self.image_view.set_new_image()
        self.update_displayed_images(True)
        self.update_displayed_images(False)

    def update_displayed_images(self,update_org_image:bool):
        img = self.get_current_image()
        if not update_org_image:
            effects = self.get_current_collection().effects
            if effects.current_history_index == len(effects.history)-1 or len(effects.history)==0:
                key = effects.get_key(img.path)
            else:
                key = effects.history[effects.current_history_index]
            if key in effects.reworked_imgs:
                moded_img = effects.reworked_imgs[key]
                cv2.imshow("read from history",moded_img)
                # effects.history.append(key)
                # self.set_mod_image(self.draw_lines(moded_img,effects.values[me.EffectType.LINES]))
                # return True
            else:
                moded_img = self.create_new_reworked_image()
                cv2.imshow("created new",moded_img)
                effects.reworked_imgs[key]=moded_img.copy()
            effects.add_new_key_to_history(key)
            effects.current_history_index+=1 # dodać przycinanie historii oraz obecny index
            img_with_drawings=self.draw_lines(moded_img,effects.values[me.EffectType.LINES.value])
            img.last_mod_pixmap = convert_cv2Image_to_QPixmap(img_with_drawings)
            self.set_mod_image(img_with_drawings)
            return True
        else:
            img_with_drawings = self.draw_lines(cv2.imread(img.path),self.get_current_collection().lines_on_org)
            img.last_mod_pixmap = convert_cv2Image_to_QPixmap(img_with_drawings)
            self.set_org_image(img_with_drawings)
            return True

    def create_new_reworked_image(self)->np.ndarray:
        effects = self.get_current_collection().effects
        if effects.values[me.EffectType.STRAIGHTENED.value]:
            img = lines_streigtening(self.get_current_image())
        else:
            img = cv2.imread(self.get_current_image().path)
        cv2.imshow("read from path",img)
        img = increase_contrast(img,effects.values[me.EffectType.CONTRAST_INTENSITY.value])
        cv2.imshow("after contrast",img)
        img = clean_page(img,effects.values[me.EffectType.UPPER_SHIFT.value],effects.values[me.EffectType.LOWER_SHIFT.value])
        cv2.imshow("after cleaning",img)
        # for stain in effects.values[me.EffectType.CORRECTIONS]:
        #     img = remove_stains(img,stain['x'],stain['y'],stain['r'])
        return img

    def draw_lines(self,image:np.ndarray,lines:Set)->np.ndarray:
        return draw_lines_and_boundaries(self.get_current_image(),image,lines)

    def set_org_image(self,image:np.ndarray):
        pixmap = convert_cv2Image_to_QPixmap(image)
        # self.image_view.view.set_left_image(pixmap)
        self.image_view.set_new_org_image(pixmap)

    def set_mod_image(self,image:np.ndarray):
        pixmap = convert_cv2Image_to_QPixmap(image)
        # self.image_view.view.set_right_image(pixmap)
        self.image_view.set_new_modified_image(pixmap)

    def get_current_pixmap(self,org:bool)->QPixmap:
        if org:
            return self.get_current_image().last_org_pixmap
        else:
            return self.get_current_image().last_mod_pixmap

    def undo(self):
        effects = self.get_current_collection().effects
        effects.undo()
        self.update_displayed_images(False)

    def redo(self):
        effects = self.get_current_collection().effects
        effects.redo()
        self.update_displayed_images(False)

    def reset(self):
        effects = self.get_current_collection().effects
        effects.reset()
        self.update_displayed_images(False)

