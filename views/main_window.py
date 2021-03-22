
from views.guielements.menu_bar import MenuBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, \
    QMenu, QAction, QFileDialog, QLabel, QMessageBox, QDockWidget, QListWidget
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Geometry
        self.setGeometry(600, 300, 800, 600)
        self.setWindowTitle("RePrinTex")

        # MenuBar
        menuBar=MenuBar(self)
        self.menuBar().addMenu(menuBar.get_file_menu())

        # Central widget
        self.setCentralWidget(QLabel())

        # Dock widgets - to jest jakieś grube i chyba można tu zrobić sporo rzeczy
        self.dock1 = QDockWidget("Files", self)
        self.dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.filesList = QListWidget(self.dock1)
        self.dock1.setWidget(self.filesList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock1)

        self.show()
