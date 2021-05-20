from threading import Lock
from typing import Any


class ControllerMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Controller(metaclass=ControllerMeta):
    def __init__(self) -> None:
        self.parent = None
        self.collection_controller = None
        self.image_preview_controller = None
        self.menu_bar_controller = None
        self.status_bar_controller = None
        self.toolbar_controller = None
        self.effects_controller = None
        self.archive_controller = None

    # Setup
    def set_image_preview_controller(self, controller):
        self.image_preview_controller = controller

    def set_collection_controller(self, controller):
        self.collection_controller = controller

    def set_menubar_controller(self, controller):
        self.menu_bar_controller = controller

    def set_statusbar_controller(self, controller):
        self.status_bar_controller = controller

    def set_toolbar_controller(self, controller):
        self.toolbar_controller = controller

    def set_effects_controller(self, controller):
        self.effects_controller = controller

    def set_archive_controller(self, controller):
        self.archive_controller = controller

    def set_parent(self, parent):
        self.parent = parent

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
