from models.page_info import PageInfo


class Image:
    img_ext = [".jpg$", ".jpeg$", ".png$", ".bmp$", ".dib$", ".jpe$", ",jp2$", ".webp$",
               ".pbm$", ".pgm$", ".ppm" ".pxm$", ".pnm$", ".pfm$", ".sr$", ".ras$",
               ".tiff$", ".tif$", ".exr$", ".hdr$", ".pic$"]

    def __init__(self, id_, path, name, pixmap=None):
        # self.id = id_
        self.path = path
        self.name = name
        self.last_org_pixmap = pixmap
        self.last_mod_pixmap = None
        self.page_info: PageInfo = None
        self.stains = []
        self.zoom = 1
        self.pixmap_position = (0, 0)
