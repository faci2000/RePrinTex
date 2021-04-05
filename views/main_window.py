from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from models.image_collection import ImageCollection
from views.guielements.central.image_preview_view import ImagePreviewView
from views.guielements.docks.collection_view import CollectionView
from views.guielements.menu.file import FileMenu
from views.guielements.toolbar.toolbar import ToolBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Geometry
        self.setGeometry(600, 300, 800, 600)
        self.setWindowTitle("RePrinTex")

        # MenuBar
        file_menu = FileMenu(self)
        self.menuBar().addMenu(file_menu.get_file_menu())

        # Toolbars
        toolbar = ToolBar(self)
        self.addToolBar(toolbar.get_toolbar())

        # Central widget
        self.image_preview_view = ImagePreviewView(self)
        self.setCentralWidget(self.image_preview_view.get_widget())

        # Dock widgets
        self.collection_view = CollectionView(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.collection_view.get_view())

        # Statusbar

        self.show()
