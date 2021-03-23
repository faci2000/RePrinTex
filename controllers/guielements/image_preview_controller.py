from PyQt5.QtCore import Qt


class ImagePreviewController:
    def __init__(self, parent, view) -> None:
        self.parent = parent
        self.view = view
        self.current_pixmap = None
        self.scale = 1

    def set_new_image(self, pixmap):
        self.current_pixmap = pixmap
        self.scale = 1
        self.view.set_image(pixmap)

    def zoom(self):
        size = self.current_pixmap.size()
        size.setWidth(int(size.width() * self.scale))
        size.setHeight(int(size.height() * self.scale))
        return self.current_pixmap.scaled(size, transformMode=Qt.SmoothTransformation)

    def zoom_in(self):
        self.scale += 0.1
        zoomed = self.zoom()
        self.view.set_image(zoomed)

    def zoom_out(self):
        self.scale -= 0.1
        zoomed = self.zoom()
        self.view.set_image(zoomed)
