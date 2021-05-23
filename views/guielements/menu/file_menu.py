from services.images_provider import ImagesProvider
from services.state_saver import save_collection, save_collections, save_view_config
from services.exporter import export_all, export_one
from PyQt5.QtWidgets import QAction, QMenu

from controllers.guielements.menu_bar_controller import MenuBarController


class FileMenu:
    def __init__(self, parent, collection_view) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent

        create_archive = QAction("&Create new image collection", self.parent)
        create_archive.triggered.connect(lambda: self.controller.create_archive(collection_view))

        open_action = QAction("&Add image to current collection", self.parent, shortcut="Ctrl+O")
        open_action.triggered.connect(lambda: self.controller.load_files())

        save_image = QAction("&Save project", self.parent)
        save_image.triggered.connect(lambda: save_collections(ImagesProvider().collections))
        save_image.triggered.connect(lambda: save_view_config(ImagesProvider()))

        remove_image = QAction("&Remove selected images", self.parent)
        remove_image.triggered.connect(lambda: self.controller.remove_images())

        remove_collection = QAction("&Remove current collection", self.parent)
        remove_collection.triggered.connect(lambda: self.controller.remove_collection())

        add_image = QAction("&Add image to collection", self.parent)
        add_image.triggered.connect(lambda: self.controller.add_image)

        export_action = QAction("&Export", self.parent, shortcut="Ctrl+S")
        export_action.triggered.connect(lambda: export_one())

        export_all_action = QAction("&Export all", self.parent)
        export_all_action.triggered.connect(lambda: export_all())

        export_menu = QMenu("&Export", self.parent)
        export_menu.addActions([export_action, export_all_action])

        self.file_menu = QMenu("&File", self.parent)
        self.file_menu.addActions([create_archive, open_action, remove_image, remove_collection, save_image])
        self.file_menu.addMenu(export_menu)

    # - File menu
    def get_file_menu(self):
        return self.file_menu
