

from models.image_collection import ImageCollection
from typing import List


def save_collections(collections_list:List[ImageCollection])->bool:
    saved_collections_paths=[]
    for collection in collections_list:
        saved_collections_paths.append({'name':collection.name,
                                        'path':save_collection(collection)})

def save_collection(collection:ImageCollection)->str:
    pass