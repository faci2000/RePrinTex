from PyQt5.QtWidgets import QAction, QMenu

from controllers.guielements.menu_bar_controller import MenuBarController


class ViewMenu:
    def __init__(self, parent) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent
        self.view_menu = QMenu("&View", self.parent)

    def get_view_menu(self):
        return self.view_menu
