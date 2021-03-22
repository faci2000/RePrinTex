import sys

from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, \
    QMenu, QAction, QFileDialog, QLabel, QMessageBox, QDockWidget, QListWidget, QListWidgetItem, QScrollArea, \
    QScrollBar, QSizePolicy


# TODO:
#  - resize obrazów przy resize okna, nwm czy do tego nie trzeba będzie z centralWidget zrobić kontenera a potem dopiero Qlabel
#  - resize obrazka na wejscie
#  - zoom
#  - save, save all, save as (tak sobie napisałam, żeby zobaczyć jak to wyjdzie, trzeba ogarnąć co nam jest potrzebne)
#  - jakie pola na menubar i ich rozwinięcia
#  - jeśli chcemy obrazki jako podgląd plików
#  - ogólnie nie wiem narazie co my tu chcemy jeszcze mieć oprócz menubar i podglądu wszystkich plików
#  - teraz zrobiłam tak, że jak się kliknie jeszcze raz open, to usuwa to co było poprzednio, nwm czy chcemy tak, czy
#  chcemy dopisywać te nowe czy rozdzielić na dwie opcje np. Open files i Add files


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.currentPixmap = None
        self.filePaths = None

        # Geometry
        self.setGeometry(600, 300, 1000, 800)
        self.setWindowTitle("RePrinTex")

        # MenuBar
        # - File menu
        openAction = QAction("&Open files", self, shortcut="Ctrl+O", triggered=self.loadFiles)
        zoomInAction = QAction("&Zoom in", self, shortcut="Ctrl+i", triggered=self.zoomIn)
        zoomOutAction = QAction("&Zoom out", self, shortcut="Ctrl+u", triggered=self.zoomOut)

        saveAction = QAction("&Save", self, shortcut="Ctrl+S", triggered=self.saveImage)
        saveAllAction = QAction("&Save All", self, triggered=self.saveAllImages)
        saveAsAction = QAction("&Save as", self, triggered=self.saveImageAs)
        saveMenu = QMenu("&Save", self)
        saveMenu.addActions([saveAction, saveAsAction, saveAllAction])

        fileMenu = QMenu("&File", self)
        fileMenu.addActions([openAction, zoomInAction, zoomOutAction])
        fileMenu.addMenu(saveMenu)
        self.menuBar().addMenu(fileMenu)

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

    # po kliknięciu 'Open' zapisuje ścieżki do wybranych plików w filePaths, tworzy QListe filesList i otwiera pierwszy obrazek
    def loadFiles(self):
        filenames, _ = QFileDialog.getOpenFileNames(self)
        if filenames:
            self.filePaths = filenames
            names = [file.split('/')[-1] for file in filenames] # to jest tylko po to, żeby trzymać w liscie ładne nazwy a nie całą ścieżke
            self.filesList.clear()

            for i in range(len(names)):
                item = QListWidgetItem(QIcon(QPixmap(self.filePaths[i])), names[i])
                self.filesList.addItem(item)

            self.filesList.currentTextChanged[str].connect(self.changeImage)
            self.openImage(filenames[0])

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

    # otwiera obrazek o danym filename
    def openImage(self, filename):
        if filename:
            image = QImage(filename)
            if image.isNull():
                QMessageBox.information(self, "Error", "Cannot load file {}.".format(filename))
                return
            self.currentPixmap = QPixmap.fromImage(image).scaled(self.width(), self.height())
            self.centralLabel.setPixmap(self.currentPixmap.scaled(
                self.centralWidget().size(), Qt.KeepAspectRatio))
        else:
            QMessageBox.information(self, "Error", "Invalid file!")

    def saveImage(self):
        pass

    def saveImageAs(self):
        pass

    def saveAllImages(self):
        pass

    # zmienia obrazek jak sie kliknie na liscie na inny
    def changeImage(self):
        idx = self.filesList.currentIndex().row()
        self.openImage(self.filePaths[idx])


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    sys.exit(app.exec_())

