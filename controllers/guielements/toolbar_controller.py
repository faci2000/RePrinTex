import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QGridLayout, QMainWindow

import imgmaneng.lines_streightening as ls
from controllers.controller import Controller
from imgmaneng.img_analyze import img_analyze
from imgmaneng.recognize_letters import recognize_letters


class ToolBarController:
    """"
            A class handling toolbar actions.

            Attributes
                parent: QMainWindow
                in_timer: QTimer
                out_timer:  QTimer
        """

    def __init__(self, parent, view) -> None:
        self.parent: QMainWindow = parent
        self.view = view
        Controller().set_toolbar_controller(self)

        self.in_timer = QTimer()
        self.out_timer = QTimer()
        self.in_timer.timeout.connect(Controller().zoom_in)
        self.out_timer.timeout.connect(Controller().zoom_out)

    def analyze_text(self):
        img_collection = Controller().get_collection()
        image = img_collection.get_current_image()
        img_analyze(image)
        cv2.imwrite("result.png", image.modified_img)
        Controller().set_new_image(image)

    def lines_straightening(self):
        img_collection = Controller().get_collection()
        image = img_collection.get_current_image()
        ls.lines_streigtening(image)
        cv2.imwrite("result.png", image.modified_img)
        img_pix = QImage("result.png")
        pixmap = QPixmap(img_pix)
        Controller().set_new_image(pixmap)

    def recognize_letters(self):
        img_collection = Controller().get_collection()
        image = img_collection.get_current_image()
        recognize_letters(image)

    def helper(self):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Help")
        dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        webEngineView = QWebEngineView(dialog)

        layout = QGridLayout()
        dialog.setLayout(layout)
        layout.addWidget(webEngineView)

        try:
            f = open('data/help/help.html', 'r')
        except (OSError, FileNotFoundError,  Exception) as e:
            Controller().communicator.error.emit("Cannot open help :c")
        else:
            with f:
                html = f.read()
                webEngineView.setHtml(html)
                dialog.show()

    def zoom_pressed(self, zoom_in):
        if zoom_in:
            self.in_timer.start(30)
        else:
            self.out_timer.start(30)

    def zoom_released(self, zoom_in):
        if zoom_in:
            self.in_timer.stop()
        else:
            self.out_timer.stop()
