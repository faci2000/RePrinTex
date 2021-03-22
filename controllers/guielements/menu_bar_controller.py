from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog,QListWidgetItem
class MenuBarController():
    def __init__(self,parent) -> None:
        self.filePaths = None
        self.currentPixmap = None
        self.parent=parent
    
        # po kliknięciu 'Open' zapisuje ścieżki do wybranych plików w filePaths, tworzy QListe filesList i otwiera pierwszy obrazek
    def loadFiles(self):
        filenames, _ = QFileDialog.getOpenFileNames(self.parent)
        if filenames:
            self.filePaths = filenames
            names = [file.split('/')[-1] for file in filenames] # to jest tylko po to, żeby trzymać w liscie ładne nazwy a nie całą ścieżke
            self.parent.filesList.clear()

            for i in range(len(names)):
                item = QListWidgetItem(QIcon(QPixmap(self.filePaths[i])), names[i])
                self.parent.filesList.addItem(item)

            self.parent.filesList.currentTextChanged[str].connect(self.changeImage)
            self.openImage(filenames[0])

    # otwiera obrazek o danym filename
    def openImage(self, filename):
        if filename:
            image = QImage(filename)
            if image.isNull():
                QMessageBox.information(self, "Error", "Cannot load file {}.".format(filename))
                return
            self.currentPixmap = QPixmap.fromImage(image).scaled(self.parent.width(), self.parent.height())
            self.parent.centralLabel.setPixmap(self.currentPixmap.scaled(
                self.parent.centralWidget().size(), Qt.KeepAspectRatio))
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
        idx = self.parent.filesList.currentIndex().row()
        self.openImage(self.filePaths[idx])