from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox, QFileDialog
class MenuBarController:
    def __init__(self,parent) -> None:
        self.filePaths = None
        self.currentPixmap = None
        self.parent=parent
    
        # po kliknięciu 'Open' zapisuje ścieżki do wybranych plików w filePaths, tworzy QListe filesList i otwiera pierwszy obrazek
    def loadFiles(self):
        print("dupa")
        filenames, _ = QFileDialog.getOpenFileNames(self.parent)
        self.filePaths = filenames
        names = [file.split('/')[-1] for file in self.parent.filenames] # to jest tylko po to, żeby trzymać w liscie ładne nazwy a nie całą ścieżke
        self.parent.filesList.clear()
        self.parent.filesList.addItems(names)
        self.parent.filesList.currentTextChanged[str].connect(self.changeImage)
        self.parent.openImage(filenames[0])

    # otwiera obrazek o danym filename
    def openImage(self, filename):
        if filename:
            image = QImage(filename)
            if image.isNull():
                QMessageBox.information(self, "Error", "Cannot load file {}.".format(filename))
                return
            self.currentPixmap = QPixmap.fromImage(image).scaled(self.width(), self.height())
            self.centralWidget().setPixmap(self.currentPixmap)
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