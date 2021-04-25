from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QLabel, QHBoxLayout, QWidget

from controllers.guielements.image_preview_controller import ImagePreviewController


def create_label(parent):
    label = QLabel(parent)
    label.setAlignment(Qt.AlignCenter)
    parent.setWidget(label)
    return label


class ImagePreviewView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ImagePreviewController(self.parent, self)

        self.layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.area_original = self.create_area(self.controller.clicked_original_action)
        self.area_modified = self.create_area(self.controller.clicked_modified_action)

        self.label_original = create_label(self.area_original)
        self.label_modified = create_label(self.area_modified)

        self.layout.addWidget(self.area_original)
        self.layout.addWidget(self.area_modified)

    def create_area(self, controller):
        area = QScrollArea(self.central_widget)
        area.setWidgetResizable(True)
        area.mouseReleaseEvent = controller
        return area

    def get_widget(self):
        return self.central_widget

    def set_new_image(self, pixmap):
        self.set_left_image(pixmap)
        self.set_right_image(pixmap)

    def set_left_image(self, pixmap):
        self.label_original.setPixmap(pixmap)

    def set_right_image(self, pixmap):
        self.label_modified.setPixmap(pixmap)

    # move which
    def move(self, v, h):
        self.area_modified.horizontalScrollBar().setValue(h)
        self.area_modified.verticalScrollBar().setValue(v)
