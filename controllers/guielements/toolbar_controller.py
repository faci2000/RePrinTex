from imgmaneng.recognize_letters import recognize_letters
from imgmaneng.img_analyze import img_analyze


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
    
    def recognize_letters(self):
        img_collection = self.parent.collection_view.controller.get_collection()
        image = img_collection.get_current_image()
        recognize_letters(image)

