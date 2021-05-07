from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QLabel

from models.image_collection import ImageCollection
from views.guielements.central.image_preview_view import ImagePreviewView
from views.guielements.docks.collection_view import CollectionView
from views.guielements.docks.effects_view import EffectsView
from views.guielements.menu.edit_menu import EditMenu
from views.guielements.menu.file_menu import FileMenu
from views.guielements.menu.view_menu import ViewMenu
from views.guielements.status.status import StatusBarView
from views.guielements.toolbar.toolbar import ToolBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        

        # Geometry
        self.setGeometry(600, 300, 1080, 720)
        self.setWindowTitle("RePrinTex")
        
        # Central widget
        self.image_preview_view = ImagePreviewView(self)
        self.setCentralWidget(self.image_preview_view.get_widget())
        
        # Dock widgets
        self.collection_view = CollectionView(self)
        self.effects_view = EffectsView(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.collection_view.get_view())
        self.addDockWidget(Qt.RightDockWidgetArea, self.effects_view.get_view())

        # MenuBar
        file_menu = FileMenu(self, self.collection_view)
        edit_menu = EditMenu(self, self.collection_view)
        view_menu = ViewMenu(self)
        self.menuBar().addMenu(file_menu.get_file_menu())
        self.menuBar().addMenu(edit_menu.get_edit_menu())
        self.menuBar().addMenu(view_menu.get_view_menu())

        # Toolbars
        toolbar = ToolBar(self)
        self.addToolBar(toolbar.get_toolbar())

        # Statusbar
        self.statusbar = StatusBarView(self)
        self.setStatusBar(self.statusbar.get_statusbar())

        self.show()
