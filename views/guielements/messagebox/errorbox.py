from PyQt5.QtWidgets import QMessageBox


class ErrorBox:
    def __init__(self, parent):
        self.parent = parent
        self.box = get_box()

    def show_error(self, msg):
        self.box.setText(msg)
        self.box.exec_()


def get_box():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Error!")
    msg.setStandardButtons(QMessageBox.Ok)
    return msg
