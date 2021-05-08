
from _typeshed import SupportsKeysAndGetItem
import json
from models.image_collection import ImageCollection
from typing import List


def read_saved_collections()->List[ImageCollection]:
    with open('collhist.json') as json_data:
        collections = json.load(json_data)
        img_collections:List[ImageCollection] =[]
        for coll in collections:
            img_collections.append(ImageCollection())