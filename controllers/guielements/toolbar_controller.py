class ToolBarController:
    def __init__(self, parent) -> None:
        self.parent = parent

    def zoom_in(self):
        self.parent.image_preview_view.controller.zoom_in()

    def zoom_out(self):
        self.parent.image_preview_view.controller.zoom_out()
