
from PyQt5.QtGui import QPixmap


class Effects: 
    def __init__(self) -> None:
        self.main_lines = False
        self.minor_lines = False
        self.text_block = False
        self.words = False
        self.letters = False
        self.upper_shift=0
        self.lower_shift=0
        self.contrast_intensity=0
