import os.path
import sys

from PyQt5.QtWidgets import QApplication

import qstylish
from views.main_window import MainWindow

if os.path.isfile("dark"):
    DARK = True
else:
    DARK = False

if __name__ == '__main__':
    app = QApplication([])
    if DARK:
        app.setStyleSheet(qstylish.dark())
    else:
        app.setStyleSheet(qstylish.light())
    win = MainWindow()
    sys.exit(app.exec_())
