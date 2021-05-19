from PyQt5.QtWidgets import QStatusBar, QLabel

from controllers.guielements.status_bar_controller import StatusBarController


class StatusBarView:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.controller = StatusBarController(self.parent, self)
        self.statusbar = QStatusBar()
        self.status_info = QLabel()
        self.statusbar.addWidget(self.status_info)

    def get_statusbar(self):
        return self.statusbar

    def setText(self, msg):
        self.status_info.setText(msg)
