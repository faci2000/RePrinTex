from views.guielements.menu.file import FileMenu
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QScrollArea, QMainWindow, QLabel, QDockWidget, QListWidget
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Geometry
        self.setGeometry(600, 300, 800, 600)
        self.setWindowTitle("RePrinTex")

        # MenuBar
        fileMenu = FileMenu(self)
        self.menuBar().addMenu(fileMenu.getFileMenu())

         # Central widget
        self.scrollArea = QScrollArea(self)
        self.setCentralWidget(self.scrollArea)
        self.centralLabel = QLabel(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.centralLabel)
        self.centralLabel.setAlignment(Qt.AlignCenter)

        # Dock widgets - to jest jakieś grube i chyba można tu zrobić sporo rzeczy
        self.dock1 = QDockWidget("Files", self)
        self.dock1.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock1)

        self.filesList = QListWidget(self.dock1)
        self.filesList.setViewMode(QListWidget.IconMode)
        self.filesList.setResizeMode(QListWidget.Adjust)
        self.filesList.setIconSize(QSize(150, 150))
        self.dock1.setWidget(self.filesList)

        # Toolbars

        # Statusbar

        self.show()
    def zoomIn(self):
        size = self.currentPixmap.size()
        size.setWidth(int(size.width() * 1.1))
        size.setHeight(int(size.height() * 1.1))
        self.currentPixmap = self.currentPixmap.scaled(size, transformMode=Qt.SmoothTransformation)
        self.centralLabel.setPixmap(self.currentPixmap)

    def zoomOut(self):
        size = self.currentPixmap.size()
        size.setWidth(int(size.width() * 0.9))
        size.setHeight(int(size.height() * 0.9))
        self.currentPixmap = self.currentPixmap.scaled(size, transformMode=Qt.SmoothTransformation)
        self.centralLabel.setPixmap(self.currentPixmap)
