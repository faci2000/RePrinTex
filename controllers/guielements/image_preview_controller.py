import services.images_provider  as sip
from imgmaneng.img_converter import convert_cv2Image_to_QPixmap
import numpy as np
import views.guielements.central.image_preview_view as vgcipv
from models.image import Image
from PyQt5.QtCore import Qt
from enum import Enum
from PyQt5.QtGui import QImage, QPixmap
from imgmaneng.img_cleaner import remove_stains

# TODO zmiana zdjecia w obrebie kolekcji - czy zapamiętujemy zoom i scrollbary czy reset
# TODO zoomowanie resetuje zmiany w modified area gdzies to trzeba trzymac, a najlepiej skopiowac cały Image to razem
#  i historia zmian do dogadania


class Area(Enum):
    ORIGINAL = 0
    MODIFIED = 1


class ImagePreviewController:
    """
    A class handling images previewing in central widget

    Attributes
        parent: QMainWindow
        view: ImagePreviewView
        current_image: Image
        active_area: Area
            left with original image or right with preview image with modifications
        preview_zoom: float
            current zoom value of modified image

    """
    def __init__(self, parent, view) -> None:
        self.parent = parent
        # Initialzie ImageProvider
        self.image_provider = sip.ImagesProvider(self)
        self.image_provider.image_view=self
        self.view:vgcipv.ImagePreviewView = view
        # image_provider.get_current_image(): Image = None
        self.active_area = Area.ORIGINAL
        self.original_zoom = 1
        self.modified_zoom = 1

    def set_new_image(self): # ustawia pierwszy raz nowe zdjecie
        # image_provider.get_current_image() = image

        self.active_area = Area.ORIGINAL
        pixmap = self.image_provider.get_current_pixmap(True)
        print(self.image_provider.get_current_image())
        print(self.image_provider.get_current_image().last_org_pixmap)

        original_area_size = self.view.area_original.size()
        self.original_zoom = original_area_size.width() * 0.9 / pixmap.size().width()
        size = self.get_size(self.original_zoom)
        self.view.set_left_image(pixmap.scaled(size, transformMode=Qt.SmoothTransformation))

        pixmap = self.image_provider.get_current_pixmap(False)

        modified_area_size = self.view.area_modified.size()
        self.modified_zoom = modified_area_size.width() * 0.9 / pixmap.size().width()
        size = self.get_size(self.modified_zoom)
        self.view.set_right_image(pixmap.scaled(size, transformMode=Qt.SmoothTransformation))

    def get_size(self, zoom):
        size = self.image_provider.get_current_pixmap(True).size()
        size.setWidth(int(size.width() * zoom))
        size.setHeight(int(size.height() * zoom))
        return size

    def set_new_modified_image(self, image:QPixmap):
        size = self.get_size(self.modified_zoom)
        pixmap = image.scaled(size, Qt.KeepAspectRatio)
        self.view.set_right_image(pixmap)
        
    def set_new_org_image(self, image:QPixmap):
        size = self.get_size(self.original_zoom)
        pixmap = image.scaled(size, Qt.KeepAspectRatio)
        self.view.set_left_image(pixmap)

    def zoom(self, alpha):
        if self.active_area == Area.ORIGINAL:
            self.original_zoom = self.original_zoom * (1 + alpha)
            size = self.get_size(self.original_zoom)
            self.view.set_left_image(self.image_provider.get_current_pixmap(True).scaled(size, transformMode=Qt.SmoothTransformation))
        else:
            self.modified_zoom = self.modified_zoom * (1 + alpha)
            size = self.get_size(self.modified_zoom)
            self.view.set_right_image(self.image_provider.get_current_pixmap(False).scaled(size, transformMode=Qt.SmoothTransformation))

    def zoom_in(self):
        self.zoom(0.07)

    def zoom_out(self):
        self.zoom(-0.07)

    def clicked_original_action(self, event):
        self.active_area = Area.ORIGINAL
        self.clicked_area_action(event)

    def clicked_modified_action(self, event):
        self.active_area = Area.MODIFIED
        self.clicked_area_action(event)

    def clicked_area_action(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.active_area == Area.ORIGINAL:
            h = self.view.area_original.horizontalScrollBar().value()
            v = self.view.area_original.verticalScrollBar().value()
            zoom = self.image_provider.get_current_image().zoom
        else:
            h = self.view.area_modified.horizontalScrollBar().value()
            v = self.view.area_modified.verticalScrollBar().value()
            zoom = self.modified_zoom

        rx = int((x + h) * 1 / zoom)
        ry = int((y + v) * 1 / zoom)
        print(rx, ry)   # position from real image in pixels

        if self.parent.effects_view.controller.is_brush_active():
            radius = self.parent.effects_view.controller.get_brush_radius()
            clean = remove_stains(self.image_provider.get_current_image(), rx, ry, radius)
            pixmap = QPixmap(QImage(clean, clean.shape[1], clean.shape[0], clean.shape[1] * 3, QImage.Format_RGB888))
            self.set_new_modified_image(pixmap)


