class Image:
    def __init__(self, idx, path, name, pixmap):
        self.id = idx
        self.path = path
        self.name = name
        self.pixmap = pixmap
        self.history = None
