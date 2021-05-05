from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QToolBar

from controllers.guielements.toolbar_controller import ToolBarController


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ToolBarController(parent)
        self.toolbar = QToolBar("Tools", self.parent)
        self.toolbar.addActions(self.get_actions())

    def get_actions(self):
        actions = [self.zoom_in(), self.zoom_out(), self.undo(), self.redo()]
        return actions

    def undo(self):

        undo = QAction(QIcon(get_icon("data/icons/undo.png")), "&Undo", self.parent)
        undo.setShortcut('Ctrl+z')
        undo.setStatusTip("Erases the last change done")
        undo.triggered.connect(lambda: self.controller.undo())
        return undo

    def redo(self):
        redo = QAction(QIcon(get_icon("data/icons/redo.png")), "&Redo", self.parent)
        redo.setShortcut('Ctrl+x')
        redo.setStatusTip("Restores the change that was previously undone")
        redo.triggered.connect(lambda: self.controller.redo())
        return redo

    def zoom_in(self):
        zoom_in = QAction(QIcon(get_icon("data/icons/zoom_in.png")), "&Zoom in", self.parent)
        zoom_in.setShortcut('Ctrl+i')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.triggered.connect(lambda: self.controller.zoom_in())  # jak sie da to od razu self.controller.zoom(1.1)
        return zoom_in

    def zoom_out(self):
        zoom_out = QAction(QIcon(get_icon("data/icons/zoom_out.png")), "&Zoom out", self.parent)
        zoom_out.setShortcut('Ctrl+o')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.triggered.connect(lambda: self.controller.zoom_out())
        return zoom_out

    def get_toolbar(self):
        return self.toolbar


def get_icon(path):
    icon = QIcon()
    icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
    return icon
