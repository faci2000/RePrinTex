import os.path

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QToolBar, QToolButton

from controllers.guielements.toolbar_controller import ToolBarController
from services.images_provider import ImagesProvider

if os.path.isfile("dark"):
    DARK = True
else:
    DARK = False


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ToolBarController(parent)
        self.toolbar = QToolBar("Tools", self.parent)
        self.toolbar.addWidget(self.zoom_in())
        self.toolbar.addWidget(self.zoom_out())
        self.toolbar.addActions(self.get_actions())

    def get_actions(self):
        actions = [self.undo(), self.redo(), self.helper()]
        return actions

    def helper(self):
        help_ = QAction(QIcon(get_icon("data/icons/help")), "&Help", self.parent)
        help_.setStatusTip("Show help")
        help_.triggered.connect(lambda: self.controller.helper())
        return help_

    def undo(self):
        undo = QAction(QIcon(get_icon("data/icons/undo")), "&Undo", self.parent)
        undo.setShortcut('Ctrl+z')
        undo.setStatusTip("Erases the last change done")
        undo.triggered.connect(lambda: ImagesProvider().undo())
        return undo

    def redo(self):
        redo = QAction(QIcon(get_icon("data/icons/redo")), "&Redo", self.parent)
        redo.setShortcut('Ctrl+x')
        redo.setStatusTip("Restores the change that was previously undone")
        redo.triggered.connect(lambda: ImagesProvider().redo())
        return redo

    def zoom_in(self):
        zoom_in = QToolButton(self.parent)
        zoom_in.setIcon(QIcon(get_icon("data/icons/zoom_in")))
        zoom_in.setShortcut('Ctrl+i')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=True))
        zoom_in.released.connect(lambda: self.controller.zoom_released(zoom_in=True))
        return zoom_in

    def zoom_out(self):
        zoom_out = QToolButton(self.parent)
        zoom_out.setIcon((QIcon(get_icon("data/icons/zoom_out"))))
        zoom_out.setShortcut('Ctrl+o')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=False))
        zoom_out.released.connect(lambda: self.controller.zoom_released(zoom_in=False))
        return zoom_out

    def get_toolbar(self):
        return self.toolbar


def get_icon(path):
    if DARK:
        new_path = path + "_light.png"
    else:
        new_path = path + "_dark.png"

    icon = QIcon()
    icon.addPixmap(QPixmap(new_path), QIcon.Normal, QIcon.Off)
    return icon
