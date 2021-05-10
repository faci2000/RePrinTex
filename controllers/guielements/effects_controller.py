from PyQt5 import Qt, QtCore
from imgmaneng.lines_boundary_drawer import draw_lines_and_boundaries
from models.effects import Effects
from PyQt5.QtGui import QImage, QPixmap, QCursor

from imgmaneng.img_cleaner import clean_page, increase_contrast
from threads.worker_decorator import multi_thread_runner


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
        self.original_effects: Effects = Effects()
        self.modified_effects: Effects = Effects()
        self.thread = None

    @multi_thread_runner
    def clean(self,):
        img = self.parent.image_preview_view.controller.current_image
        img = clean_page(img, self.modified_effects.upper_shift, self.modified_effects.lower_shift)
        img = QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
        self.parent.image_preview_view.controller.set_new_modified_image(img)

    @multi_thread_runner
    def contrast(self):
        img = self.parent.image_preview_view.controller.current_image
        img = increase_contrast(img, self.modified_effects.contrast_intensity)
        img = QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
        self.parent.image_preview_view.controller.set_new_modified_image(img)

    def straighten_lines(self):
        self.parent.errorbox.show_error("Aj nie działa")

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

    @multi_thread_runner
    def updated_drawing_effects(self, update_org: bool):
        self.parent.statusbar.setText("Cleaning")
        if update_org:
            img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image, self.original_effects)
            self.parent.image_preview_view.controller.view.set_left_image(img)
        else:
            print(self.parent.image_preview_view.controller.current_image)
            img = self.contrast(self.parent.image_preview_view.controller.current_image)
            # img = self.clean(img)
            img = QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
            # img = draw_lines_and_boundaries(self.parent.image_preview_view.controller.current_image, self.modified_effects, img)
            self.parent.image_preview_view.controller.set_new_modified_image(img)
        self.parent.statusbar.setText("Success")

    def change_cursor(self):
        if self.is_brush_active():
            pixmap = QPixmap("data/cursors/circle_cursor.png")
            size = 2.1*self.get_brush_radius()*self.parent.image_preview_view.controller.modified_zoom
            pixmap = pixmap.scaled(size, size)
            cursor = QCursor(pixmap, -1, -1)
            self.parent.setCursor(cursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

