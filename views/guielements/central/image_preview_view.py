from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QWidget, QSplitter, QPushButton, QHBoxLayout, QSizePolicy

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

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.area_original = self.create_area()
        self.area_modified = self.create_area()

        self.label_original = create_label(self.area_original, self.controller.clicked_original_action)
        self.label_modified = create_label(self.area_modified, self.controller.clicked_modified_action)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.splitter.addWidget(self.area_original)
        self.splitter.addWidget(self.area_modified)

        self.layout.addWidget(self.splitter)

        self.add_buttons()

    def add_buttons(self):
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)

        next_button = QPushButton()
        next_button.setText("Next image")
        # next_button.clicked.connect()

        prev_button = QPushButton()
        prev_button.setText("Previous image")
        # prev_button.clicked.connect()

        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)
        button_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.layout.addWidget(button_widget)

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
