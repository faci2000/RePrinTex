import sys
import os.path
from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow
import qstylish
import os.path

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
