import traceback
from threading import Lock
from typing import Any, List, Set

import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

import models.effects as me
import models.image_collection as mic
from controllers.controller import Controller
from controllers.guielements.image_preview_controller import ImagePreviewController
from imgmaneng.img_cleaner import clean_page, increase_contrast, remove_stains
from imgmaneng.img_converter import convert_cv2Image_to_QPixmap
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from imgmaneng.lines_streightening import lines_streigtening
from models.image import Image


class ImagesProviderMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwargs)
                self._instances[self] = instance
        return self._instances[self]


class EmptyCollectionsListException(Exception):
    pass


class EmptyCollectionException(Exception):
    pass


class ImagesProvider(metaclass=ImagesProviderMeta):
    def __init__(self, image_view: ImagePreviewController = None) -> None:
        import controllers.guielements.collection_controller as cgcc
        self.collections: List[mic.ImageCollection] = []
        self.current_collection_index: int = None
        self.current_image_index: int = None
        self.image_view: ImagePreviewController = image_view
        self.image_selector: cgcc.CollectionController = None

    def load_data(self):
        import services.state_reader as ssr
        self.collections = ssr.read_saved_collections()
        print(self.collections)
        ssr.read_view_config(self)
        try:
            self.image_selector.fill_name_combobox()
            self.image_selector.view.collections_list.setCurrentIndex(self.current_collection_index)
            self.image_selector.fill_collection_list_view(self.get_current_collection())
            self.set_image_to_display()
        except Exception:
            traceback.print_exc()

    def get_recently_added_collection(self) -> mic.ImageCollection:
        if len(self.collections) == 0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[len(self.collections) - 1]

    def get_current_collection(self) -> mic.ImageCollection:
        if len(self.collections) == 0:
            raise EmptyCollectionsListException("List of collections is empty. Add some image collection first.")
        else:
            return self.collections[self.current_collection_index]

    def get_current_collection_effects(self) -> me.Effects:
        return self.get_current_collection().effects

    def get_current_collection_org_lines(self) -> Set:
        return self.get_current_collection().lines_on_org

    def get_current_image(self) -> Image:
        collection = self.get_current_collection()
        if len(collection.collection) == 0:
            raise EmptyCollectionException("Image collection is empty. Add some images to collection first.")
        else:
            return collection.collection[self.current_image_index]

    def image_exists(self):
        try:
            self.get_current_image()
            return True
        except EmptyCollectionException:
            return False

    def change_current_image(self, new_image_index: int) -> Image:
        old_index = self.current_image_index
        try:
            self.current_image_index = new_image_index
            return self.get_current_image()
        except IndexError:
            print("Index out of bounds.")
            self.current_image_index = old_index
            return self.get_current_image()

    def change_current_collection(self, new_collection_index: int = None,
                                  new_collection_text: str = None) -> mic.ImageCollection:
        old_index = self.current_collection_index
        try:
            if new_collection_index:
                self.current_collection_index = new_collection_index
            else:
                for i in range(len(self.collections)):
                    if self.collections[i].name == new_collection_text:
                        self.current_collection_index = i
                        break
            Controller().update_redo_undo(self.get_current_collection_effects())
            return self.get_current_collection()
        except:
            print("Index out of bounds.")
            self.current_collection_index = old_index
            return self.get_current_collection()

    def add_new_collection(self,
                           new_image_collection: mic.ImageCollection) -> bool:  # return true if changed current collection
        print(new_image_collection.name)
        self.collections.append(new_image_collection)  # otherwise return false

        if self.current_collection_index is None:
            self.current_collection_index = len(self.collections) - 1
            self.image_selector.view.collections_list.setCurrentIndex(self.current_collection_index)
            self.image_selector.change_collection(new_image_collection.name)
            return True
        else:
            return False

    def add_new_image(self, image: Image):
        self.get_current_collection().add_image(Image)
        self.change_current_image(len(self.get_current_collection().collection) - 1)
        self.set_image_to_display()

    def change_current_collection_to_added_recently(self) -> None:
        self.image_selector.change_collection(self.collections[len(self.collections) - 1].name)

    def set_image_to_display(self):
        image = cv2.imread(self.get_current_image().path)
        self.get_current_image().last_org_pixmap = convert_cv2Image_to_QPixmap(image)
        print(self.get_current_image())
        print(self.get_current_image().last_org_pixmap)
        print("set pixmap mod")
        self.get_current_image().last_mod_pixmap = convert_cv2Image_to_QPixmap(image)
        self.image_view.set_new_image()
        self.update_displayed_images(True, True)
        self.update_displayed_images(False, True)

    def update_displayed_images(self, update_org_image: bool,changes:bool):
        try:
            img = self.get_current_image()
            if not update_org_image:
                effects = self.get_current_collection().effects
                print("EFFECTS HISTORY: ",effects.history, effects.current_history_index)
                print("EFFECTS VALUES: ",effects.values[me.EffectType.LINES.value], effects.values[me.EffectType.LOWER_SHIFT.value],
                      effects.values[me.EffectType.UPPER_SHIFT.value],
                      effects.values[me.EffectType.CONTRAST_INTENSITY.value],
                      effects.values[me.EffectType.STRAIGHTENED.value],
                      img.stains)# ,

                key = effects.get_key(img)
                print("SET KEY: ",key)
                if key in effects.reworked_imgs:
                    moded_img = effects.reworked_imgs[key].copy()
                    # cv2.imshow("read from history", moded_img)
                    # effects.history.append(key)
                    # self.set_mod_image(self.draw_lines(moded_img,effects.values[me.EffectType.LINES]))
                    # return True
                else:
                    moded_img = self.create_new_reworked_image()
                    # cv2.imshow("created new",moded_img)
                    print("# MODED_IMG",id(moded_img))
                    effects.reworked_imgs[key] = moded_img.copy()
                    print("# COPIED_IMG",id(effects.reworked_imgs[key]))
                if changes:
                    effects.add_new_key_to_history(key)
                    effects.current_history_index += 1  # dodać przycinanie historii oraz obecny index
                img_with_drawings = self.draw_lines(moded_img, effects.values[me.EffectType.LINES.value])
                print("# IMG_WITH_DRAWINGS",id(img_with_drawings))
                img.last_mod_pixmap = convert_cv2Image_to_QPixmap(img_with_drawings)
                self.set_mod_image(img_with_drawings)
                return True
            else:
                img_with_drawings = self.draw_lines(cv2.imread(img.path), self.get_current_collection().lines_on_org)
                img.last_mod_pixmap = convert_cv2Image_to_QPixmap(img_with_drawings)
                self.set_org_image(img_with_drawings)
                return True
        except EmptyCollectionException as e:
            Controller().communicator.error.emit(str(e))
            return

    def create_new_reworked_image(self, original_image=None) -> np.ndarray:
        if original_image is None:
            original_image = self.get_current_image()

        effects = self.get_current_collection().effects
        if effects.values[me.EffectType.STRAIGHTENED.value]:
            img = lines_streigtening(original_image)
        else:
            img = cv2.imread(original_image.path)
        # cv2.imshow("read from path",img)
        if effects.values[me.EffectType.UPPER_SHIFT.value] and effects.values[me.EffectType.LOWER_SHIFT.value]:
            img = clean_page(img, effects.values[me.EffectType.UPPER_SHIFT.value],
                             effects.values[me.EffectType.LOWER_SHIFT.value])

        if effects.values[me.EffectType.CONTRAST_INTENSITY.value]:
            img = increase_contrast(img, effects.values[me.EffectType.CONTRAST_INTENSITY.value])
        # cv2.imshow("after contrast",img)

        # cv2.imshow("after cleaning",img)
        if original_image.stains:
            for stain in original_image.stains:
                img = remove_stains(img, stain['x'], stain['y'], stain['r'])
        return img

    def draw_lines(self, image: np.ndarray, lines: Set) -> np.ndarray:
        return draw_lines_and_boundaries(self.get_current_image(), image, lines)

    def set_org_image(self, image: np.ndarray):
        pixmap = convert_cv2Image_to_QPixmap(image)
        # self.image_view.view.set_left_image(pixmap)
        self.image_view.set_new_org_image(pixmap)

    def set_mod_image(self, image: np.ndarray):
        Controller().update_redo_undo(self.get_current_collection_effects())

        pixmap = convert_cv2Image_to_QPixmap(image)
        # self.image_view.view.set_right_image(pixmap)
        self.image_view.set_new_modified_image(pixmap)

    def get_current_pixmap(self, org: bool) -> QPixmap:
        if org:
            return self.get_current_image().last_org_pixmap
        else:
            return self.get_current_image().last_mod_pixmap

    def undo(self):
        effects = self.get_current_collection().effects
        effects.undo(self.get_current_image())
        self.update_displayed_images(False, False)
        Controller().change_redo_button(enabled=True)

    def redo(self):
        effects = self.get_current_collection().effects
        effects.redo(self.get_current_image())
        self.update_displayed_images(False, False)
        Controller().change_undo_button(enabled=True)

    def reset(self):
        effects = self.get_current_collection().effects
        effects.reset(self.get_current_image())
        self.update_displayed_images(False, False)
        Controller().change_undo_button(enabled=True)
        Controller().change_redo_button(enabled=True)

    def change_image_to_next(self):
        index = self.image_selector.view.files_list.currentIndex().row()
        size = self.image_selector.view.files_list.count()
        print("Image change next: ",index,size,(index+1)%size)
        self.image_selector.view.files_list.setCurrentRow((index+1)%size)
        self.change_current_image((index+1)%size)
        self.set_image_to_display()

    def change_image_to_prev(self):
        index = self.image_selector.view.files_list.currentIndex().row()
        size = self.image_selector.view.files_list.count()
        print("Image change prev: ",index,size,(index-1)%size)
        self.image_selector.view.files_list.setCurrentRow((index-1)%size)
        self.change_current_image((index-1)%size)
        self.set_image_to_display()

    def get_current_image_name(self):
        return self.get_current_image().name

