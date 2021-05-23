from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import services.images_provider as sip
import views.guielements.central.image_preview_view as vgcipv
from controllers.controller import Controller
from models.effects import EffectType


# TODO zmiana zdjecia w obrebie kolekcji - czy zapamiętujemy zoom i scrollbary czy reset
# TODO zoomowanie resetuje zmiany w modified area gdzies to trzeba trzymac, a najlepiej skopiowac cały Image to razem
#  i historia zmian do dogadania
from threads.worker_decorator import multi_thread_runner


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
        self.image_provider.image_view = self
        self.view: vgcipv.ImagePreviewView = view
        # image_provider.get_current_image(): Image = None
        self.active_area = Area.ORIGINAL
        self.original_zoom = 1
        self.modified_zoom = 1

        Controller().set_image_preview_controller(self)

    def set_new_image(self):  # ustawia pierwszy raz nowe zdjecie
        # image_provider.get_current_image() = image

        self.active_area = Area.ORIGINAL
        pixmap = self.image_provider.get_current_pixmap(True)
        print(self.image_provider.get_current_image())
        print(self.image_provider.get_current_image().last_org_pixmap)

        original_area_size = self.view.area_original.size()
        self.original_zoom = original_area_size.width() / pixmap.size().width()
        size = self.get_size(self.original_zoom)
        self.view.set_left_image(pixmap.scaled(size, transformMode=Qt.SmoothTransformation))

        pixmap = self.image_provider.get_current_pixmap(False)

        modified_area_size = self.view.area_modified.size()
        self.modified_zoom = modified_area_size.width() / pixmap.size().width()
        size = self.get_size(self.modified_zoom)
        self.view.set_right_image(pixmap.scaled(size, transformMode=Qt.SmoothTransformation))

    def get_size(self, zoom):
        size = self.image_provider.get_current_pixmap(True).size()
        size.setWidth(int(size.width() * zoom))
        size.setHeight(int(size.height() * zoom))
        return size

    def set_new_modified_image(self, image: QPixmap):
        size = self.get_size(self.modified_zoom)
        pixmap = image.scaled(size, Qt.KeepAspectRatio)
        self.current_modified = image
        self.view.set_right_image(pixmap)

    def set_new_org_image(self, image: QPixmap):
        size = self.get_size(self.original_zoom)
        pixmap = image.scaled(size, Qt.KeepAspectRatio)
        self.view.set_left_image(pixmap)

    def zoom(self, alpha):
        if self.active_area == Area.ORIGINAL:
            self.original_zoom = self.original_zoom * (1 + alpha)
            size = self.get_size(self.original_zoom)
            self.view.set_left_image(
                self.image_provider.get_current_pixmap(True).scaled(size, transformMode=Qt.SmoothTransformation))
        else:
            self.modified_zoom = self.modified_zoom * (1 + alpha)
            size = self.get_size(self.modified_zoom)
            self.view.set_right_image(
                self.image_provider.get_current_pixmap(False).scaled(size, transformMode=Qt.SmoothTransformation))

        if Controller().is_brush_active():
            Controller().change_cursor()

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
        try:
            if not sip.ImagesProvider().image_exists():
                return

            x = event.pos().x()
            y = event.pos().y()

            if self.active_area == Area.ORIGINAL:
                pixmap = self.image_provider.get_current_pixmap(True)
                height = self.view.label_original.height()
                width = self.view.label_original.width()
                zoom = self.original_zoom
                h_ratio = (self.view.area_original.horizontalScrollBar().value() * 1.0 / max(
                    self.view.area_original.horizontalScrollBar().maximum(), 1))
                v_ratio = (self.view.area_original.verticalScrollBar().value() * 1.0 / max(
                    self.view.area_original.verticalScrollBar().maximum(), 1))

            else:
                pixmap = self.image_provider.get_current_pixmap(False)
                height = self.view.label_modified.height()
                width = self.view.label_modified.width()
                zoom = self.modified_zoom
                h_ratio = self.view.area_modified.horizontalScrollBar().value() * 1.0 / max(
                    self.view.area_modified.horizontalScrollBar().maximum(), 1)
                v_ratio = self.view.area_modified.verticalScrollBar().value() * 1.0 / max(
                    self.view.area_modified.verticalScrollBar().maximum(), 1)

            h_res = x + h_ratio * max(0, zoom * pixmap.width() - width) - max(0, width - zoom * pixmap.width()) // 2
            v_res = y + v_ratio * max(0, zoom * pixmap.height() - height) - max(0, height - zoom * pixmap.height()) // 2

            rx = int(h_res * 1.0 / zoom)
            ry = int(v_res * 1.0 / zoom)

            if Controller().is_brush_active() and rx >= 0 and ry >= 0 and rx < pixmap.width() and ry < pixmap.height():
                radius = Controller().get_brush_radius()
                Controller().change_effects({'effect_type': EffectType.CORRECTIONS,
                                             'org': False,
                                             'values': [{'type': EffectType.CORRECTIONS,
                                                         'value': {'x': rx, 'y': ry, 'r': radius}}]})
        except sip.EmptyCollectionException as e:
            Controller().communicator.error.emit("Cannot perform an action!")
