from PyQt5 import QtWidgets


class ArchiveCreatorController:
    
    def __init__(self,archive_creator) -> None:
        self.archive_creator = archive_creator
    
    def open_file_browser(self,path_box):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        path_box.setText('{}'.format(directory))

    def 