from imgmaneng.img_cleaner import clean_page, increase_contrast
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

    def undo(self):
        pass

    def analyze_text(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        img_analyze(image)
    
    def recognize_letters(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        recognize_letters(image)

    def clean(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        cleaned = clean_page(image)
        cleaned_qt = QImage(cleaned, cleaned.shape[1], cleaned.shape[0], cleaned.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap(cleaned_qt)
        self.parent.image_preview_view.controller.set_new_image(pixmap)

    def contrast(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        enhanced = increase_contrast(image)
        enhanced_qt = QImage(enhanced, enhanced.shape[1], enhanced.shape[0], enhanced.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap(enhanced_qt)
        self.parent.image_preview_view.controller.set_new_image(pixmap)

