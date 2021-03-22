from controllers.guielements.menu_bar_controller import MenuBarController
from PyQt5.QtWidgets import QAction,QMenu
class MenuBar:
    def __init__(self,parent)->None:
        self.controller = MenuBarController(parent)
        self.parent=parent
    
    # - File menu
    def get_file_menu(self):
        openAction = QAction("&Open files", self.parent ,shortcut="Ctrl+O", triggered=self.controller.loadFiles())
        saveAction = QAction("&Save", self.parent ,shortcut="Ctrl+S", triggered=self.controller.saveImage)
        saveAllAction = QAction("&Save All",  self.parent ,triggered=self.controller.saveAllImages)
        saveAsAction = QAction("&Save as",  self.parent ,triggered=self.controller.saveImageAs)
        saveMenu = QMenu("&Save",self.parent)
        saveMenu.addActions([saveAction, saveAsAction, saveAllAction])

        fileMenu = QMenu("&File",self.parent)
        fileMenu.addActions([openAction])
        fileMenu.addMenu(saveMenu)
        return fileMenu
