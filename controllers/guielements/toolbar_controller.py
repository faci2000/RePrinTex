import cv2
from imgmaneng.recognize_letters import recognize_letters
from imgmaneng.img_analyze import img_analyze
from PyQt5.QtGui import QImage, QPixmap



class ToolBarController:
    def __init__(self, parent) -> None:
        self.parent = parent

    def zoom_in(self):
        self.parent.image_preview_view.controller.zoom_in()

    def zoom_out(self):
        self.parent.image_preview_view.controller.zoom_out()

    def analyze_text(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        img_analyze(image)
        cv2.imwrite("result.png", image.modified_img)
        img_pix = QImage("result.png")
        pixmap = QPixmap(img_pix)
        self.parent.image_preview_view.controller.set_new_image(pixmap)

    
    def recognize_letters(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        recognize_letters(image)

