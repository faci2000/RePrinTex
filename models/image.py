from models.page_info import PageInfo


class Image:
    def __init__(self, id_, path, name, pixmap):
        self.id = id_
        self.path = path
        self.name = name
        self.pixmap = pixmap
        self.history = None
        self.page_info: PageInfo = None
        self.modified_img = None
        self.zoom = 1
        self.pixmap_position = (0, 0)
