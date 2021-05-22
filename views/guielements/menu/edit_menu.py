from PyQt5.QtWidgets import QAction, QMenu

from controllers.controller import Controller
from controllers.guielements.menu_bar_controller import MenuBarController
from services.images_provider import ImagesProvider


class EditMenu:
    def __init__(self, parent, collection_view) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent

        straighten_lines = QAction("&Straighten lines", self.parent)
        straighten_lines.triggered.connect(lambda: self.parent.effects_view.straighten_lines.setChecked(True))

        clean_page = QAction("&Clean page", self.parent)
        clean_page.triggered.connect(lambda: self.controller.clean_page())

        contrast_page = QAction("&Increase contrast", self.parent)
        contrast_page.triggered.connect(lambda: self.controller.increase_contrast())

        remove_stains = QAction("&Remove stains", self.parent)
        remove_stains.triggered.connect(lambda: self.controller.remove_stains())

        apply = QAction("&Apply", self.parent)
        apply.triggered.connect(lambda: Controller().apply())

        apply_to_all = QAction("&Apply to all", self.parent)
        apply_to_all.triggered.connect(lambda: Controller().apply_to_all())

        reset = QAction("&Reset", self.parent)
        reset.triggered.connect(lambda: ImagesProvider().reset())

        effects_menu = QMenu("&Effects", self.parent)
        effects_menu.addActions([straighten_lines, clean_page, contrast_page, remove_stains])

        self.edit_menu = QMenu("&Edit", self.parent)
        self.edit_menu.addActions([apply, apply_to_all, reset])
        self.edit_menu.addMenu(effects_menu)

    def get_edit_menu(self):
        return self.edit_menu
