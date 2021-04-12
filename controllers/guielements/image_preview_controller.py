from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from imgmaneng.img_cleaner import remove_stains


class ImagePreviewController:
    def __init__(self, parent, view) -> None:
        self.parent = parent
        self.view = view
        self.current_pixmap = None
        self.scale = 1
        self.alpha = 1

    def set_new_image(self, pixmap):
        self.current_pixmap = pixmap
        self.scale = 1
        self.alpha = 1
        self.view.set_image(pixmap)

    def zoom(self):
        size = self.current_pixmap.size()
        size.setWidth(int(size.width() * self.scale))
        size.setHeight(int(size.height() * self.scale))
        return self.current_pixmap.scaled(size, transformMode=Qt.SmoothTransformation)

    def zoom_in(self):
        self.scale += 0.1 * self.alpha
        self.alpha /= 1.01
        zoomed = self.zoom()
        self.view.set_image(zoomed)

    def zoom_out(self):
        self.scale -= 0.1 * self.alpha
        self.alpha /= 1.01
        zoomed = self.zoom()
        self.view.set_image(zoomed)

    def go_to(self, zoom, vertical, horizontal):
        self.scale = zoom
        zoomed = self.zoom()
        self.view.set_image(zoomed)
        self.view.move(vertical, horizontal)

    def clicked_action(self, event):
        x = event.pos().x()
        y = event.pos().y()
        h = self.view.area.horizontalScrollBar().value()
        v = self.view.area.verticalScrollBar().value()

        rx = (x + h) * 1/self.scale
        ry = (y + v) * 1/self.scale

        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        enhanced = remove_stains(image, rx, ry)
        enhanced_qt = QImage(enhanced, enhanced.shape[1], enhanced.shape[0], enhanced.shape[1] * 3,
                             QImage.Format_RGB888)
        pixmap = QPixmap(enhanced_qt)
        self.parent.image_preview_view.controller.set_new_image(pixmap)

