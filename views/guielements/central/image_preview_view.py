from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea, QLabel, QHBoxLayout, QWidget, QSplitter

import controllers.guielements.image_preview_controller as cgipc


def create_label(parent, controller):
    label = QLabel(parent)
    label.setAlignment(Qt.AlignCenter)
    label.mouseReleaseEvent = controller
    parent.setWidget(label)
    return label


class ImagePreviewView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = cgipc.ImagePreviewController(self.parent, self)

        self.layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.area_original = self.create_area()
        self.area_modified = self.create_area()

        self.label_original = create_label(self.area_original, self.controller.clicked_original_action)
        self.label_modified = create_label(self.area_modified, self.controller.clicked_modified_action)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.area_original)
        self.splitter.addWidget(self.area_modified)

        self.layout.addWidget(self.splitter)

    def create_area(self):
        area = QScrollArea(self.central_widget)
        area.setWidgetResizable(True)
        return area

    def get_widget(self):
        return self.central_widget

    def set_new_image(self, pixmap: QPixmap):
        self.set_left_image(pixmap)
        self.set_right_image(pixmap)

    def set_left_image(self, pixmap: QPixmap):
        self.label_original.setPixmap(pixmap)

    def set_right_image(self, pixmap: QPixmap):
        self.label_modified.setPixmap(pixmap)

    # move which
    def move(self, v, h):
        self.area_modified.horizontalScrollBar().setValue(h)
        self.area_modified.verticalScrollBar().setValue(v)
