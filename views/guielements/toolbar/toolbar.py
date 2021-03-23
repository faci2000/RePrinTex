from PyQt5.QtWidgets import QAction, QToolBar

from controllers.guielements.toolbar_controller import ToolBarController


# TODO zoom nie działa xD


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ToolBarController(parent)
        self.toolbar = QToolBar("Tools", self.parent)
        self.toolbar.addActions(self.get_actions())

    def get_actions(self):
        actions = [self.zoom_in(), self.zoom_out()]
        return actions

    def zoom_in(self):
        zoom_in = QAction("&Zoom in", self.parent)
        # zoomIn = QAction(QIcon("zoomIn.bmp"),"Zoom in",self) <- too jak zrobimy ikonki kiedyś

        zoom_in.setShortcut('Ctrl+u')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.triggered.connect(lambda: self.controller.zoom_in())  # jak sie da to od razu self.controller.zoom(1.1)
        return zoom_in

    def zoom_out(self):
        zoom_out = QAction("&Zoom out", self.parent)
        # zoomOut = QAction(QIcon("zoomOut.bmp"),"Zoom out",self) <- too jak zrobimy ikonki kiedyś

        zoom_out.setShortcut('Ctrl+i')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.triggered.connect(lambda: self.controller.zoom_out())
        return zoom_out

    def rotate(self):
        pass

    def undo(self):
        pass

    def get_toolbar(self):
        return self.toolbar
