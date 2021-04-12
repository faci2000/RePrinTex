from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QLabel

from controllers.guielements.image_preview_controller import ImagePreviewController


class ImagePreviewView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ImagePreviewController(self.parent, self)

        self.area = QScrollArea(self.parent)
        self.label = QLabel(self.area)

        self.area.setWidgetResizable(True)
        self.area.setWidget(self.label)
        self.area.mouseReleaseEvent = self.controller.clicked_action
        self.label.setAlignment(Qt.AlignCenter)

    def get_widget(self):
        return self.area

    def set_image(self, pixmap):
        self.label.setPixmap(pixmap)

    def move(self, v, h):
        self.area.horizontalScrollBar().setValue(h)
        self.area.verticalScrollBar().setValue(v)
