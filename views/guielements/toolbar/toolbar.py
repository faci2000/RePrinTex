import os.path

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QToolBar, QToolButton, QMainWindow

from controllers.controller import Controller
from controllers.guielements.toolbar_controller import ToolBarController
from services.images_provider import ImagesProvider
from services.state_reader import read_style_config

if os.path.isfile("dark"):
    DARK = True
else:
    DARK = False


class ToolBar:
    """"
        A class creating toolbar view.

        Attributes
            parent: QMainWindow
            controller: ToolBarController
            toolbar:  QToolBar

        Methods:
            get_toolbar() -> QToolBar
                returns complete toolbar with undo, redo, zoom in, zoom out and help actions
    """

    def __init__(self, parent):
        self.parent: QMainWindow = parent
        self.controller: ToolBarController = ToolBarController(parent, self)
        self.toolbar: QToolBar = QToolBar("Tools", self.parent)

        self.undo_button = self.get_undo()
        self.redo_button = self.get_redo()

        self._add_buttons()
        self.toolbar.addAction(self._helper())

    def _add_buttons(self):
        self.toolbar.addWidget(self._zoom_in())
        self.toolbar.addWidget(self._zoom_out())
        self.toolbar.addWidget(self.undo_button)
        self.toolbar.addWidget(self.redo_button)

    def _helper(self):
        help_ = QAction("&Help", self.parent)
        set_icon("data/icons/help", help_, "Help")
        help_.setStatusTip("Show help")
        help_.triggered.connect(lambda: self.controller.helper())
        return help_

    def get_undo(self):
        undo_button = QToolButton(self.parent)
        set_icon("data/icons/undo", undo_button, "Undo")
        undo_button.setShortcut('Ctrl+z')
        undo_button.setStatusTip("Erases the last change done")
        undo_button.clicked.connect(lambda: ImagesProvider().undo())
        undo_button.setEnabled(False)
        return undo_button

    def get_redo(self):
        redo_button = QToolButton(self.parent)
        set_icon("data/icons/redo", redo_button, "Redo")
        redo_button.setShortcut('Ctrl+x')
        redo_button.setStatusTip("Restores the change that was previously undone")
        redo_button.clicked.connect(lambda: ImagesProvider().redo())
        redo_button.setEnabled(False)
        return redo_button

    def _zoom_in(self):
        zoom_in = QToolButton(self.parent)
        set_icon("data/icons/zoom_in", zoom_in, "Zoom in")
        zoom_in.setShortcut('Ctrl+i')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=True))
        zoom_in.released.connect(lambda: self.controller.zoom_released(zoom_in=True))
        return zoom_in

    def _zoom_out(self):
        zoom_out = QToolButton(self.parent)
        set_icon("data/icons/zoom_out", zoom_out, "Zoom out")
        zoom_out.setShortcut('Ctrl+o')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.pressed.connect(lambda: self.controller.zoom_pressed(zoom_in=False))
        zoom_out.released.connect(lambda: self.controller.zoom_released(zoom_in=False))
        return zoom_out

    def get_toolbar(self):
        return self.toolbar


def set_icon(path, object_, name):
    """ Adds icon or name to existing QAction or QToolButton """

    try:
        if read_style_config() == "dark":
            new_path = path + "_light.png"
        else:
            new_path = path + "_dark.png"

        if not os.path.isfile(new_path):
            raise FileNotFoundError

        icon = QIcon()
        icon.addPixmap(QPixmap(new_path), QIcon.Normal, QIcon.Off)
        object_.setIcon((QIcon(new_path)))

    except (OSError, FileNotFoundError,  Exception) as e:
        if type(object_) is QToolButton:
            object_.setText(name)
        Controller().communicator.error.emit("Cannot load some toolbar icons :c")
