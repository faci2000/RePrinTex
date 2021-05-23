from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QMessageBox

from controllers.controller import Controller
from views.guielements.effects_layout import add_clean, add_contrast, add_stains


class Dialogs:
    def __init__(self, parent):
        self.parent = parent
        self.controller = Controller().effects_controller

        self.clean_dialog = self.get_clean_dialog()
        self.contrast_dialog = self.get_contrast_dialog()
        self.stains_dialog = self.get_stains_dialog()
        self.style_dialog = self.get_style_dialog()

    def get_clean_dialog(self):
        dialog, layout = self.create_empty_dialog("Clean page")
        add_clean(self, dialog, layout)
        dialog.setLayout(layout)
        return dialog

    def get_contrast_dialog(self):
        dialog, layout = self.create_empty_dialog("Manage contrast")
        add_contrast(self, dialog, layout)
        dialog.setLayout(layout)
        return dialog

    def get_stains_dialog(self):
        dialog, layout = self.create_empty_dialog("Remove stains")
        add_stains(self, layout)
        dialog.setLayout(layout)
        return dialog

    def get_style_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Style changed")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText("Style will changed next time you open the app.")
        return msg

    def open_style(self):
        self.style_dialog.show()

    def open_clean(self):
        self.clean_dialog.show()

    def open_contrast(self):
        self.contrast_dialog.show()

    def open_stains(self):
        self.stains_dialog.show()

    def create_empty_dialog(self, title):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle(title)
        dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        dialog.setModal(False)
        layout = QGridLayout(dialog)

        return dialog, layout


