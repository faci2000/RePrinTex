from controllers.guielements.archive_creator_controller import ArchiveCreatorController
import typing
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.QtWidgets import QBoxLayout, QDialog, QDialogButtonBox


class ArchiveCreator(QDialog):
    def __init__(self, collection_view):
        super(QDialog, self).__init__()
        self.controller = ArchiveCreatorController(self, collection_view)

        layout = QBoxLayout(QBoxLayout.TopToBottom, self)

        name_label = QtWidgets.QLabel()
        name_label.setText("Archive name:")
        layout.addWidget(name_label)

        name_box = QtWidgets.QLineEdit()
        # name_box.textChanged.connect(lambda: self.controller.set_name(str(path_box.currentText()),name_box))
        layout.addWidget(name_box)

        path_label = QtWidgets.QLabel()
        path_label.setText("Archive path:")

        layout.addWidget(path_label)
        path_box = QtWidgets.QComboBox()
        path_box.currentTextChanged.connect(lambda: self.controller.set_name(str(path_box.currentText()),name_box))
        layout.addWidget(path_box)

        browse_button = QtWidgets.QToolButton()
        browse_button.clicked.connect(lambda: self.controller.open_file_browser(path_box))
        browse_button.setText("Browse")
        layout.addWidget(browse_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.accepted.connect(lambda: self.controller.set_name(str(path_box.currentText()),name_box))
        buttons.accepted.connect(lambda: self.controller.save_config())
        buttons.accepted.connect(lambda: self.controller.create_new_collection(str(path_box.currentText())))
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.controller.on_start(path_box)
