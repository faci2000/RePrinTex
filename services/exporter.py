from models.image import Image
from imgmaneng.img_cleaner import clean_page, increase_contrast
from imgmaneng.lines_streightening import lines_streigtening
from models.effects import EffectType
import cv2
from services.images_provider import ImagesProvider


def apply_to_all():
    img_prov = ImagesProvider()
    effects = img_prov.get_current_collection().effects
    for image in img_prov.get_current_collection().collection:
        export_one(img_prov,image,"./temp/"+img_prov.get_current_collection().detail_file_name+"/"+image.name+".png")

def export_one(img_prov,image:Image,path:str):
    effects = img_prov.get_current_collection().effects
    if effects.values[EffectType.STRAIGHTENED.value]:
        img = lines_streigtening(image)
    else:
        img = cv2.imread(image.path)
    img = increase_contrast(img,effects.values[EffectType.CONTRAST_INTENSITY.value])
    img = clean_page(img,effects.values[EffectType.UPPER_SHIFT.value],effects.values[EffectType.LOWER_SHIFT.value])
    cv2.imwrite(path,img)

def export_all(given_path):
    img_prov = ImagesProvider()
    effects = img_prov.get_current_collection().effects
    for image in img_prov.get_current_collection().collection:
        export_one(given_path+"/"+img_prov.get_current_collection().name+"/"+image.name+".png",image)
