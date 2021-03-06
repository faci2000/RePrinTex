from threading import Lock
from typing import Any

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QDialog, QListWidget, QListWidgetItem, QVBoxLayout, QLabel, QPushButton

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
    error = pyqtSignal(str)


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

        self.remove_list = None

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

    def apply(self):
        self.effects_controller.apply()

    def apply_to_all(self):
        self.effects_controller.apply_to_all()

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
        return self.collection_controller.get_collection()

    def get_collections(self):
        return self.collection_controller.collections

    def add_collection(self, path, name):
        self.collection_controller.add_collection(path, name)

    def add_image(self, file_paths):
        self.collection_controller.add_images(file_paths)

    def remove_images(self):
        self.collection_controller.remove_images()

    def remove_collection(self):
        self.collection_controller.remove_collection()

    # Toolbar controller
    def change_undo_button(self, enabled=True):
        self.toolbar_controller.view.undo_button.setEnabled(enabled)

    def change_redo_button(self, enabled=True):
        self.toolbar_controller.view.redo_button.setEnabled(enabled)

    def update_redo_undo(self, effects):
        if effects.current_history_index == 0:
            self.change_undo_button(False)
        else:
            self.change_undo_button(True)
        if effects.current_history_index < len(effects.history) - 1:
            self.change_redo_button(True)
        else:
            self.change_redo_button(False)

    # Errors | Messages
    def show_error(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(message)
        msg.exec_()


