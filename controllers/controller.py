from threading import Lock
from typing import Any

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox


class ControllerMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Communicator(QObject):
    error = pyqtSignal()


class Controller(metaclass=ControllerMeta):
    def __init__(self) -> None:
        self.parent = None
        self.collection_controller = None
        self.image_preview_controller = None
        self.menubar_controller = None
        self.toolbar_controller = None
        self.effects_controller = None
        self.archive_controller = None
        self.statusbar = None

        self.communicator = Communicator()
        self.communicator.error.connect(self.show_error)

    # Setup
    def set_image_preview_controller(self, controller):
        self.image_preview_controller = controller

    def set_collection_controller(self, controller):
        self.collection_controller = controller

    def set_menubar_controller(self, controller):
        self.menubar_controller = controller

    def set_toolbar_controller(self, controller):
        self.toolbar_controller = controller

    def set_effects_controller(self, controller):
        self.effects_controller = controller

    def set_archive_controller(self, controller):
        self.archive_controller = controller

    def set_parent(self, parent):
        self.parent = parent
        self.statusbar = self.parent.statusBar()

    # Effects controller
    def is_brush_active(self):
        return self.effects_controller.is_brush_active()

    def get_brush_radius(self):
        return self.effects_controller.get_brush_radius()

    def change_effects(self, args):
        self.effects_controller.change_effects(args)

    def get_effects_controller(self):
        return self.effects_controller

    def change_cursor(self):
        self.effects_controller.change_cursor()

    # Image preview controller
    def set_new_image(self, img):
        self.image_preview_controller.set_new_image(img)

    def zoom_in(self):
        self.image_preview_controller.zoom_in()

    def zoom_out(self):
        self.image_preview_controller.zoom_out()

    def get_modified_zoom(self):
        return self.image_preview_controller.modified_zoom

    # Collection Controller
    def get_collection(self):
        self.collection_controller.get_collection()

    def get_collections(self):
        return self.collection_controller.collections

    def add_collection(self, path, name):
        self.collection_controller.add_collection(path, name)

    def create_collection(self, file_paths):
        self.collection_controller.create_collection(file_paths)

    # Errors | Messages
    def show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText("Eluwina")
        msg.exec_()
