from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from controllers.controller import Controller
from services.images_provider import ImagesProvider
from services.state_saver import save_collections, save_view_config
from views.guielements.central.image_preview_view import ImagePreviewView
from views.guielements.docks.collection_view import CollectionView
from views.guielements.docks.effects_view import EffectsView
from views.guielements.menu.edit_menu import EditMenu
from views.guielements.menu.file_menu import FileMenu
from views.guielements.menu.view_menu import ViewMenu
from views.guielements.messagebox.errorbox import ErrorBox
from views.guielements.toolbar.toolbar import ToolBar


# Jak tak się zastanowić, to nie jest dobrym podejściem startować wszystko z
# z widoku, jeśli zostanie czasu na rózne głupoty, to wartobyłoby to przerobić
# żeby był jakiś przyzwoity konfigurator, który startuje i uzupełnia główne okno,
# a także uruchamia poszczególne usługi tj. ImageProvider, który jest teraz 
# startowany z CollectionView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #Icon
        self.setWindowIcon(QtGui.QIcon('data/icons/Logo2.png'))
        # Geometry
        self.setGeometry(600, 300, 1080, 720)
        self.setWindowTitle("RePrinTex")

        # Controller
        Controller().set_parent(self)

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
        self.view_menu = ViewMenu(self)
        self.menuBar().addMenu(file_menu.get_file_menu())
        self.menuBar().addMenu(edit_menu.get_edit_menu())
        self.menuBar().addMenu(self.view_menu.get_view_menu())

        # Toolbars
        toolbar = ToolBar(self)
        self.addToolBar(toolbar.get_toolbar())

        # Images provider init
        ImagesProvider().load_data()

        # Error handling
        self.errorbox = ErrorBox(self)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        img_prov = ImagesProvider()
        save_collections(img_prov.collections)
        save_view_config(img_prov)
