from PyQt5.QtWidgets import QAction, QMenu

from controllers.guielements.menu_bar_controller import MenuBarController


class FileMenu:
    def __init__(self, parent) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent
        open_action = QAction("&Open files", self.parent, shortcut="Ctrl+O")
        open_action.triggered.connect(lambda: self.controller.load_files())

        save_action = QAction("&Save", self.parent, shortcut="Ctrl+S")
        save_action.triggered.connect(lambda: self.controller.save_image)

        save_all_action = QAction("&Save All", self.parent)
        save_all_action.triggered.connect(lambda: self.controller.save_all_images)

        save_as_action = QAction("&Save as", self.parent, triggered=self.controller.save_image_as)
        save_as_action.triggered.connect(lambda: self.controller.save_all_images)

        save_menu = QMenu("&Save", self.parent)
        save_menu.addActions([save_action, save_as_action, save_all_action])

        self.file_menu = QMenu("&File", self.parent)
        self.file_menu.addActions([open_action])
        self.file_menu.addMenu(save_menu)

    # - File menu
    def get_file_menu(self):
        return self.file_menu
