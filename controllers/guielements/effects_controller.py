from imgmaneng.img_converter import QImage2CV, convert_QPixmap_to_cv2Image, convert_cv2Image_to_QPixmap
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from models.effects import Effects
import cv2
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap

from imgmaneng.img_cleaner import clean_page, increase_contrast
from threads.Worker import Worker


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
        self.original_effects:Effects = Effects()
        self.modified_effects:Effects = Effects()

    def clean(self, img):
        clean = clean_page(img, self.modified_effects.upper_shift, self.modified_effects.lower_shift)
        return clean

    def contrast(self, img):
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

    def updated_drawing_effects(self, update_org: bool):
        if update_org:  
            img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image, self.original_effects)
            self.parent.image_preview_view.controller.view.set_left_image(img)
        else:
            img = self.contrast(self.parent.image_preview_view.controller.current_image)
            img = self.clean(img)
            img = QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
            # img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image, self.modified_effects, img)
            self.parent.image_preview_view.controller.current_image.history.append(img)
            self.parent.image_preview_view.controller.set_new_modified_image(img)




    


