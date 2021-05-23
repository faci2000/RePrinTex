from PyQt5 import QtWidgets
import cv2
from controllers.controller import Controller
from models.image import Image
from services.images_provider import EmptyCollectionException, ImagesProvider
import os


def apply_to_all():
    img_prov = ImagesProvider()
    effects = img_prov.get_current_collection().effects
    try:
        os.mkdir("./tmp/" + img_prov.get_current_collection().detail_file_name)
    except FileExistsError:
        pass
    for image in img_prov.get_current_collection().collection:
        no = str(img_prov.collections.index(img_prov.get_current_collection())) + str(img_prov.get_current_collection().collection.index(image))
        export_one( image,
                   "./tmp/" + img_prov.get_current_collection().detail_file_name + "/" + image.name + "_rpt" + no + ".png")


def export_one(image: Image=None, path: str=None):
    try:
        if image==None and path==None:
            directory = str(QtWidgets.QFileDialog.getExistingDirectory())
            image = ImagesProvider().get_current_image()
            no = str(ImagesProvider().collections.index(ImagesProvider().get_current_collection())) + str(ImagesProvider().get_current_collection().collection.index(image))
            path = directory + "/" + ImagesProvider().get_current_collection().name + "/" + image.name + "_rpt" + no + ".png"
            try:
                os.mkdir(directory + "/" + ImagesProvider().get_current_collection().name)
            except FileExistsError:
                pass
        img = ImagesProvider().create_new_reworked_image(image)
        print("Saving image: ",path)
        if(cv2.imwrite(path, img)):
            print("Image saved sucessfuly.")
    except EmptyCollectionException as e:
        Controller().communicator.error.emit(str(e))
        return

    except OSError:
        Controller().communicator.error.emit("Cannot create a directory!")
        return


def export_all():
    img_prov = ImagesProvider()
    try:
        effects = img_prov.get_current_collection().effects
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        try:
            os.mkdir(directory + "/" + img_prov.get_current_collection().name)
        except FileExistsError:
            pass
        for image in img_prov.get_current_collection().collection:
            no = str(img_prov.collections.index(img_prov.get_current_collection())) + str(img_prov.get_current_collection().collection.index(image))
            export_one(image, directory + "/" + img_prov.get_current_collection().name + "/" + image.name + "_rpt" + no + ".png")
    except EmptyCollectionException as e:
        Controller().communicator.error.emit(str(e))
        return

    except OSError:
        Controller().communicator.error.emit("Cannot create a directory!")
        return

# @multi_thread_runner
# def apply(self, image=None, path=None):
#     if image is None:
#         image = ImagesProvider().create_new_reworked_image()
#     if path is None:
#         name = ImagesProvider().get_current_image_name()
#         directory = str(QtWidgets.QFileDialog.getExistingDirectory())
#         path = directory + "/" + name + "_converted.png"
#     cv2.imwrite(path, image)

# @multi_thread_runner
# def apply_to_all(self):
#     try:
#         C = ImagesProvider().get_current_collection()
#         directory = str(QtWidgets.QFileDialog.getExistingDirectory())
#         new_dir = directory + "/" + C.name
#         os.mkdir(new_dir)

#     for image in C.collection:
#         new_image = ImagesProvider().create_new_reworked_image(image)
#         path = new_dir + "/" + image.name + "_converted.png"
#         self.apply(new_image, path)