from enum import Enum
from models.image import Image

import numpy as np
import json

class Lines(Enum):
    __order__ = 'MAIN_LINES MINOR_LINES TEXT_BLOCK WORDS LETTERS'
    MAIN_LINES = 'Main lines'
    MINOR_LINES = 'Minor lines'
    TEXT_BLOCK = 'Text block'
    WORDS = 'Words'
    LETTERS = 'Letters'


class EffectType(Enum):
    LINES = 'lines'
    UPPER_SHIFT = 'upper_shift'
    LOWER_SHIFT = 'lower_shift'
    CONTRAST_INTENSITY = 'contrast_intensity'
    CORRECTIONS = 'corrections'
    STRAIGHTENED = 'straightened'


class Effects:
    def __init__(self) -> None:
        self.values = {}
        self.values[EffectType.LINES.value] = {}
        self.values[EffectType.UPPER_SHIFT.value] = None
        self.values[EffectType.LOWER_SHIFT.value] = None
        self.values[EffectType.CONTRAST_INTENSITY.value] = None
        self.values[EffectType.STRAIGHTENED.value] = False
        # self.values[EffectType.CORRECTIONS.value] = []
        self.current_history_index = 0
        self.history = []
        self.reworked_imgs = {}

    def get_key(self, img:Image):
        return (img.path + '|' + str(self.values[EffectType.STRAIGHTENED.value]) + '|' + str(
            self.values[EffectType.CONTRAST_INTENSITY.value]) + '|' +
                str(self.values[EffectType.UPPER_SHIFT.value]) + '|' + str(
                    self.values[EffectType.LOWER_SHIFT.value]) +  '|' +
                str(img.stains))
                # str(self.values[EffectType.CORRECTIONS.value]))

    def parse_effects_values(self,key:str,img:Image):
        splited_key = key.split('|')
        self.values[EffectType.STRAIGHTENED.value] = ("True" == splited_key[1])
        if splited_key[2] != 'None':
            self.values[EffectType.CONTRAST_INTENSITY.value] = float(splited_key[2])
        else:
            self.values[EffectType.CONTRAST_INTENSITY.value] = None

        if splited_key[3] != 'None':
            self.values[EffectType.UPPER_SHIFT.value] = float(splited_key[3])
        else:
            self.values[EffectType.UPPER_SHIFT.value] = None

        if splited_key[4] != 'None':
            self.values[EffectType.LOWER_SHIFT.value] = float(splited_key[4])
        else:
            self.values[EffectType.LOWER_SHIFT.value] = None
        img.stains=[]
        if splited_key[5] != '[]':
            corr_objs = splited_key[5][1:-1].split(', ')
            for i in range(0,len(corr_objs),3):
                img.stains.append({'x': int(corr_objs[i].split(' ')[1]),
                                   'y': int(corr_objs[i+1].split(' ')[1]),
                                   'r': int(corr_objs[i+2].split(' ')[1][:-1])})


    def undo(self,img:Image):
        if self.current_history_index > 0:
            print("CURRENT INDEX:",self.current_history_index)
            self.current_history_index -= 1
            print("CURRENT INDEX:",self.current_history_index)
            self.parse_effects_values(self.history[self.current_history_index-1],img)
        else:
            raise IndexError

    def redo(self, img: Image):
        if self.current_history_index < len(self.history):
            self.current_history_index += 1
            self.parse_effects_values(self.history[self.current_history_index-1],img)
        else:
            raise IndexError

    def add_new_key_to_history(self, key) -> np.ndarray:
        if self.current_history_index < len(self.history) - 1:
            while self.current_history_index < len(self.history) - 1:
                self.history.pop(len(self.history) - 1)
        self.history.append(key)

    def reset(self, img: Image) -> np.ndarray:
        zero_key = self.history[0]
        self.add_new_key_to_history(zero_key)
        self.parse_effects_values(zero_key,img)
