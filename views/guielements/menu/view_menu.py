import os.path

from PyQt5.QtWidgets import QMenu, QAction

from controllers.guielements.menu_bar_controller import MenuBarController

if os.path.isfile("dark"):
    DARK = True
else:
    DARK = False


class ViewMenu:
    def __init__(self, parent) -> None:
        self.controller = MenuBarController(parent)
        self.parent = parent
        self.view_menu = QMenu("&View", self.parent)

        change_style = QMenu("&Change window style", self.parent)
        self.light = QAction("&Light theme", self.parent, checkable=True, checked=(not DARK))
        self.dark = QAction("&Dark theme", self.parent, checkable=True, checked=DARK)
        self.dark.triggered.connect(lambda: self.controller.change_style(dark=True))
        self.light.triggered.connect(lambda: self.controller.change_style(dark=False))

        change_style.addActions([self.light, self.dark])
        self.view_menu.addMenu(change_style)

    def get_view_menu(self):
        return self.view_menu
