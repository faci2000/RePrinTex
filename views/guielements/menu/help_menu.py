from PyQt5.QtWidgets import QAction, QMenu

from controllers.guielements.menu_bar_controller import MenuBarController


class HelpMenu:
    def __init__(self, parent) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent
        self.help_menu = QMenu("&Help", self.parent)

    def get_help_menu(self):
        return self.help_menu
