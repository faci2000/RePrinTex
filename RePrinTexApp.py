import os.path
import sys

from PyQt5.QtWidgets import QApplication

import qstylish
from services.state_reader import read_style_config
from views.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    style = read_style_config()
    if style == "dark":
        app.setStyleSheet(qstylish.dark())
    else:
        app.setStyleSheet(qstylish.light())
    win = MainWindow()
    sys.exit(app.exec_())
