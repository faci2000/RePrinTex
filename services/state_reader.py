import json
from typing import List

import services.images_provider as sip
from models.effects import EffectType
from models.image import Image
from models.image_collection import ImageCollection
from models.page_info import PageInfo


def read_saved_collections() -> List[ImageCollection]:
    try:
        with open('./data/coll.json', 'r') as json_data:
            collections = json.load(json_data)
            img_collections: List[ImageCollection] = []
            for coll in collections:
                img_collections.append(read_saved_collection_data(coll["path"]))
            return img_collections
    except FileNotFoundError:
        return []


def read_saved_collection_data(path: str) -> ImageCollection:
    # print(path)
    path = './data/colldet/' + path
    with open(path, 'r') as json_data:
        collection = json.load(json_data)
        img_coll = ImageCollection(name=collection['name'])
        img_coll.detail_file_name = path.split('/')[-1][:-5]
        img_coll.effects.values = collection['effects']
        img_coll.effects.values[EffectType.LINES.value] = {}
        img_coll.effects.values[EffectType.LINES.value] = []
        # print(collection)
        for img in collection['images']:
            # print(img)
            img_coll.add_image(Image(1, path=img['path'], name=img['name']))

            if 'page_info' in img:
                img_coll.collection[len(img_coll.collection) - 1].page_info = PageInfo()
                img_coll.collection[len(img_coll.collection) - 1].page_info.text_block = img['page_info']['text_block']
                img_coll.collection[len(img_coll.collection) - 1].page_info.letters = img['page_info']['letters']
                img_coll.collection[len(img_coll.collection) - 1].page_info.lines = img['page_info']['lines']
                img_coll.collection[len(img_coll.collection) - 1].page_info.text_lines = img['page_info']['text_lines']
        return img_coll


def read_view_config(image_provider: sip.ImagesProvider):
    try:
        with open('./data/viewcfg.json', 'r') as json_data:
            data = json.load(json_data)
            image_provider.current_collection_index = data['current_collection_index']
            image_provider.current_image_index = data['current_image_index']
    except FileNotFoundError:
        return
