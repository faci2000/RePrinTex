from controllers.guielements.archive_creator_controller import ArchiveCreatorController
import typing
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.QtWidgets import QBoxLayout, QDialog, QDialogButtonBox

class ArchiveCreator(QDialog):
    def __init__(self):
        super(QDialog,self).__init__()
        self.controller = ArchiveCreatorController(self)

        layout  = QBoxLayout(QBoxLayout.TopToBottom,self)

        path_label = QtWidgets.QLabel()
        path_label.setText("Archive path:")
        layout.addWidget(path_label)

        path_box = QtWidgets.QLineEdit()
        path_box.setEnabled(False)
        layout.addWidget(path_box)

        browse_button = QtWidgets.QToolButton()
        browse_button.clicked.connect(lambda: self.controller.open_file_browser(path_box))
        layout.addWidget(browse_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


        

    