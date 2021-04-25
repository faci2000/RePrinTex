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

    def clean(self):
        current = self.parent.image_preview_view.controller.current_image
        upper_shift = self.view.clean_slider_light.value()
        lower_shift = self.view.clean_slider_dark.value()

        clean = clean_page(current, upper_shift, lower_shift)
        pixmap = QPixmap(QImage(clean, clean.shape[1], clean.shape[0], clean.shape[1] * 3, QImage.Format_RGB888))
        self.parent.image_preview_view.controller.set_new_modified_image(pixmap)

    def contrast(self):
        current = self.parent.image_preview_view.controller.current_image
        intensity = self.view.contrast_slider.value() * 1.0 / 10

        clean = increase_contrast(current, intensity)
        pixmap = QPixmap(QImage(clean, clean.shape[1], clean.shape[0], clean.shape[1] * 3, QImage.Format_RGB888))
        self.parent.image_preview_view.controller.set_new_modified_image(pixmap)

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


