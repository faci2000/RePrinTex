from imgmaneng.img_converter import convert_cv2Image_to_QPixmap
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from imgmaneng.lines_streightening import lines_streigtening
from imgmaneng.img_cleaner import clean_page, increase_contrast, remove_stains
import cv2
from models.effects import EffectType, Effects
from controllers.guielements.image_preview_controller import ImagePreviewController
from models.image import Image
from typing import Any, List, Set
from models.image_collection import ImageCollection
from threading import Lock, Thread
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
        self.collections:List[ImageCollection] = []
        self.current_collection_index:int = None
        self.current_image_index:int = None
        self.image_view:ImagePreviewController = image_view

    def get_recently_added_collection(self)->ImageCollection:
        if len(self.collections)==0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[len(self.collections)-1]

    def get_current_collection(self)->ImageCollection:
        if len(self.collections)==0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[self.current_collection_index]

    def get_current_collection_effects(self)->Effects:
        return self.get_current_collection().effects

    def get_current_collection_org_lines(self)->Set:
        return self.get_current_collection().lines_on_org

    def get_current_image(self)->Image:
        collection = self.get_current_collection()
        if len(collection)==0:
            raise EmptyCollectionException("Image collection is empty. Add some images to collection first.")
        else:
            return self.get_current_collection()[self.current_image_index]

    def add_new_collection(self,new_image_collection:ImageCollection)->bool: # return true if changed current collection
        self.collections.append(new_image_collection)                        # otherwise return false 
        if self.current_collection_index == None:
            self.current_collection_index = len(self.collections)-1
            return True
        else:
            return False

    def change_current_collection_to_added_recently(self)->None:
        self.current_collection_index = len(self.collections)-1
        if len(self.get_current_collection())==0:
            self.current_image_index=None
        else:
            self.current_image_index=1

    def update_displayed_images(self,update_org_image:bool):
        img = self.get_current_image()
        if not update_org_image:
            effects = self.get_current_collection().effects
            key = effects.get_key(img.path)
            if key in effects.reworked_imgs:
                moded_img = effects.get_reworked_img[key]
                # effects.history.append(key)
                # self.set_mod_image(self.draw_lines(moded_img,effects.values[EffectType.LINES]))
                # return True
            else:
                moded_img = self.create_new_reworked_image()
                effects.reworked_imgs[key]=moded_img
            effects.history.append(key)
            self.set_mod_image(self.draw_lines(moded_img,effects.values[EffectType.LINES]))
            return True
        else:
            self.set_org_image(self.draw_lines(cv2.imread(img.path),self.get_current_collection().lines_on_org))
            return True

    def create_new_reworked_image(self)->np.ndarray:
        effects = self.get_current_collection().effects
        if effects.values[EffectType.STRAIGHTENED]:
            img = lines_streigtening(self.get_current_image())
        else:
            img = cv2.imread(self.get_current_image().path)

        img = increase_contrast(img,effects.values[EffectType.CONTRAST_INTENSITY])
        img = clean_page(img,effects.values[EffectType.UPPER_SHIFT],effects.values[EffectType.LOWER_SHIFT])
        # for stain in effects.values[EffectType.CORRECTIONS]:
        #     img = remove_stains(img,stain['x'],stain['y'],stain['r'])
        return img

    def draw_lines(self,image:np.ndarray,lines:Set)->np.ndarray:
        return draw_lines_and_boundaries(self.get_current_image(),image,lines)

    def set_org_image(self,image:np.ndarray):
        pixmap = convert_cv2Image_to_QPixmap(image)
        self.image_view.view.set_left_image(pixmap)

    def set_mod_image(self,image:np.ndarray):
        pixmap = convert_cv2Image_to_QPixmap(image)
        self.image_view.view.set_right_image(pixmap)

