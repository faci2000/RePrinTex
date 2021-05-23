import json

from PyQt5 import QtWidgets

from controllers.controller import Controller
from views.guielements.docks.collection_view import CollectionView


class ArchiveCreatorController:

    def __init__(self, archive_creator, collection_view) -> None:
        self.archive_creator = archive_creator
        self.collections = {}
        self.collection_view: CollectionView = collection_view

        Controller().set_archive_controller(self)

    def open_file_browser(self, path_box: QtWidgets.QComboBox):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        path_box.addItem('{}'.format(directory))
        path_box.setCurrentIndex(path_box.count() - 1)

    def on_start(self, path_box: QtWidgets.QComboBox):
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                for coll in data['collections']:
                    self.collections[coll['path']] = coll['name']
                    path_box.addItem(coll['path'])
        except:
            data = {}
            data['collections'] = []
            with open('config.json', 'w') as outfile:
                json.dump(data, outfile)

    def set_name(self, value, name_box: QtWidgets.QLineEdit):
        # print(value)
        if value != "" and value is not None and value in self.collections:
            name_box.setText(self.collections[value])
        # elif name_box.text() != "" and value != "":
        #     self.collections[value] = name_box.text()

    def save_name(self, value, name_box: QtWidgets.QLineEdit):
        self.collections[value] = name_box.text()

    def save_config(self):
        with open('config.json') as json_file:
            data = json.load(json_file)

        data['collections'] = []
        for key, value in self.collections.items():
            data['collections'].append({'path': key, 'name': value})
            print({'name': value, 'path': key})
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)

    def create_new_collection(self, path, name):
        for coll in Controller().get_collections():
            if coll.path == path:
                return
        Controller().add_collection(path, name)
