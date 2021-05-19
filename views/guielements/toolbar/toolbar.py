from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QToolBar, QToolButton

from controllers.guielements.toolbar_controller import ToolBarController
from services.images_provider import ImagesProvider

import os.path

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
        if DARK:
            path = "data/icons/help_light.png"
        else:
            path = "data/icons/help_dark.png"

        help_ = QAction(QIcon(get_icon(path)), "&Help", self.parent)
        help_.setStatusTip("Show help")
        help_.triggered.connect(lambda: self.controller.helper())
        return help_

    def undo(self):
        if DARK:
            path = "data/icons/undo_light.png"
        else:
            path = "data/icons/undo_dark.png"
        undo = QAction(QIcon(get_icon(path)), "&Undo", self.parent)
        undo.setShortcut('Ctrl+z')
        undo.setStatusTip("Erases the last change done")
        undo.triggered.connect(lambda: ImagesProvider().undo())
        return undo

    def redo(self):
        if DARK:
            path = "data/icons/redo_light.png"
        else:
            path = "data/icons/redo_dark.png"
        redo = QAction(QIcon(get_icon(path)), "&Redo", self.parent)
        redo.setShortcut('Ctrl+x')
        redo.setStatusTip("Restores the change that was previously undone")
        redo.triggered.connect(lambda: ImagesProvider().redo())
        return redo

    def zoom_in(self):
        if DARK:
            path = "data/icons/zoom_in_light.png"
        else:
            path = "data/icons/zoom_in_dark.png"
        zoom_in = QToolButton(self.parent)
        zoom_in.setIcon(QIcon(get_icon(path)))
        zoom_in.setShortcut('Ctrl+i')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=True))
        zoom_in.released.connect(lambda: self.controller.zoom_released(zoom_in=True))
        return zoom_in

    def zoom_out(self):
        if DARK:
            path = "data/icons/zoom_out_light.png"
        else:
            path = "data/icons/zoom_out_dark.png"
        zoom_out = QToolButton(self.parent)
        zoom_out.setIcon((QIcon(get_icon(path))))
        zoom_out.setShortcut('Ctrl+o')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=False))
        zoom_out.released.connect(lambda: self.controller.zoom_released(zoom_in=False))
        return zoom_out

    def get_toolbar(self):
        return self.toolbar


def get_icon(path):
    icon = QIcon()
    icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
    return icon
