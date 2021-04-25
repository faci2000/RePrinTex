from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget, QListWidget, QListWidgetItem

from controllers.guielements.collection_controller import CollectionController


class CollectionView:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.controller = CollectionController(parent, self)
        self.dock = QDockWidget("Collections", self.parent)

        self.files_list = QListWidget(self.dock)
        self.files_list.setViewMode(QListWidget.IconMode)
        self.files_list.setResizeMode(QListWidget.Adjust)
        self.files_list.setIconSize(QSize(50, 50))
        self.files_list.currentTextChanged[str].connect(lambda: self.controller.change_image())

        self.dock.setWidget(self.files_list)

    def clear(self):
        self.files_list.clear()

    def add_image_icon(self, pixmap, name):
        item = QListWidgetItem(QIcon(pixmap), name)
        self.files_list.addItem(item)

    def get_view(self):
        return self.dock
