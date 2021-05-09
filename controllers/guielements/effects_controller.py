from services.images_provider import ImagesProvider
from imgmaneng.img_converter import QImage2CV, convert_QPixmap_to_cv2Image, convert_cv2Image_to_QPixmap
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from models.effects import EffectType, Effects, Lines
import cv2
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap

from imgmaneng.img_cleaner import clean_page, increase_contrast


class EffectsController:
    """
    A class for handling effects on images

    Attributes
        parent: QMainWindow
        view: EffectsView

    """

    def __init__(self, parent, view) -> None:
        self.parent = parent
        self.view = view
        #img = parent.image_preview_view.controller.current_image
        self.image_provider = ImagesProvider()

    def clean(self,img):
        clean = clean_page(img, self.modified_effects.upper_shift, self.modified_effects.lower_shift)
        return clean

    def contrast(self,img):
        clean = increase_contrast(img, self.modified_effects.contrast_intensity)
        return clean

    def straighten_lines(self):
        pass

    def apply(self):
        pass

    def apply_all(self):
        pass

    def reset(self):
        pass

    def is_brush_active(self):
        return self.view.stains_button.isChecked()

    def get_brush_radius(self):
        return self.view.stains_slider.value()

    def change_effects(self,effects_to_change): # {effect_type:EffectType,type:Line,org:bool ,value:bool}
        print(effects_to_change)
        effects = self.image_provider.get_current_collection_effects()
        if effects_to_change['org']:
            if effects_to_change['value']:
                self.image_provider.get_current_collection_org_lines().add(effects_to_change['type'])
            else:
                self.image_provider.get_current_collection_org_lines().remove(effects_to_change['type'])
        elif effects_to_change['effect_type'] == EffectType.LINES:
            if effects_to_change['type'] not in effects.values[EffectType.LINES.value]:
                effects.values[EffectType.LINES.value][effects_to_change['type']]=True
            else:
                effects.values[EffectType.LINES.value].pop(effects_to_change['type'])
            print(effects.values[EffectType.LINES.value])
        else:
            for eff in effects_to_change['values']:
                effects.values[eff['type'].value] = eff['value']
        self.image_provider.update_displayed_images(effects_to_change['org'])

    def updated_drawing_effects(self, update_org: bool):
        if update_org:
            img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image, self.original_effects)
            self.parent.image_preview_view.controller.view.set_left_image(img)
        else:
            img = self.contrast(self.parent.image_preview_view.controller.current_image)
            img = self.clean(img)
            # img = QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
            img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image,self.modified_effects,img)
            self.parent.image_preview_view.controller.set_new_modified_image(img)




