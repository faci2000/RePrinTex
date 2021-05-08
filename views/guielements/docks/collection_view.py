from services.images_provider import ImagesProvider
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QDockWidget, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from controllers.guielements.collection_controller import CollectionController


class CollectionView:
    def __init__(self, parent) -> None:
        # Initialzie ImageProvider
        self.image_provider = ImagesProvider(self)
        self.parent = parent
        self.controller = CollectionController(parent, self)
        self.dock = QDockWidget("Collections", self.parent)
        self.multiwidget = QWidget()
        self.vbox = QVBoxLayout()

        self.collections_list = QComboBox(self.dock)
        self.vbox.addWidget(self.collections_list)

        self.files_list = QListWidget(self.dock)
        self.files_list.setViewMode(QListWidget.IconMode)
        self.files_list.setResizeMode(QListWidget.Adjust)
        self.files_list.setIconSize(QSize(50, 50))
        self.files_list.currentTextChanged[str].connect(lambda: self.controller.change_image())
        self.vbox.addWidget(self.files_list)

        self.multiwidget.setLayout(self.vbox)
        self.dock.setWidget(self.multiwidget)

    def clear(self):
        self.files_list.clear()

    def add_image_icon(self, pixmap, name):
        item = QListWidgetItem(QIcon(pixmap), name)
        self.files_list.addItem(item)

    def get_view(self):
        return self.dock
