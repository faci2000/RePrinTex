from PyQt5.QtWidgets import QAction, QMenu

from controllers.guielements.menu_bar_controller import MenuBarController


class EditMenu:
    def __init__(self, parent, collection_view) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent

        straighten_lines = QAction("&Straighten lines", self.parent)
        clean_page = QAction("&Clean page", self.parent)
        contrast_page = QAction("&Increase contrast", self.parent)
        remove_stains = QAction("&Remove stains", self.parent)
        undo = QAction("&Undo", self.parent)
        redo = QAction("&Redo", self.parent)
        apply = QAction("&Apply", self.parent)
        apply_to_all = QAction("&Apply to all", self.parent)
        reset = QAction("&Reset", self.parent)

        # export_all_action.triggered.connect(lambda: self.controller.export_all_images)
        # export_as_action = QAction("&Export as", self.parent, triggered=self.controller.export_image_as)

        effects_menu = QMenu("&Effects", self.parent)
        effects_menu.addActions([straighten_lines, clean_page, contrast_page, remove_stains])

        self.edit_menu = QMenu("&Edit", self.parent)
        self.edit_menu.addActions([undo, redo, apply, apply_to_all, reset])
        self.edit_menu.addMenu(effects_menu)

    def get_edit_menu(self):
        return self.edit_menu
