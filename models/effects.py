import numpy as np

from enum import Enum
class Lines(Enum):
    __order__ = 'MAIN_LINES MINOR_LINES TEXT_BLOCK WORDS LETTERS'
    MAIN_LINES='Main lines'
    MINOR_LINES='Minor lines'
    TEXT_BLOCK='Text block'
    WORDS='Words'
    LETTERS='Letters'

class EffectType(Enum):
    LINES='lines'
    UPPER_SHIFT='upper_shift'
    LOWER_SHIFT='lower_shift'
    CONTRAST_INTENSITY='contrast_intensity'
    CORRECTIONS='corrections'
    STRAIGHTENED='straightened'
class Effects:
    def __init__(self) -> None:
        self.values={}
        self.values[EffectType.LINES.value]={}
        self.values[EffectType.UPPER_SHIFT.value]=0
        self.values[EffectType.LOWER_SHIFT.value]=0
        self.values[EffectType.CONTRAST_INTENSITY.value]=0
        self.values[EffectType.STRAIGHTENED.value]=False
        self.values[EffectType.CORRECTIONS.value]={}
        self.current_history_index = 0
        self.history = []
        self.reworked_imgs = {}

    def get_key(self, img_path):
        return (img_path + '|' + str(self.values[EffectType.STRAIGHTENED.value]) + '|' + str(self.values[EffectType.CONTRAST_INTENSITY.value]) +
                str(self.values[EffectType.UPPER_SHIFT.value]) + '|' + str(self.values[EffectType.LOWER_SHIFT.value]) + '|' +
                str(self.values[EffectType.CORRECTIONS.value]))

    def undo(self):
        if self.current_history_index>0:
            self.current_history_index-=1
        else:
            raise IndexError

    def redo(self)->np.ndarray:
        if self.current_history_index<len(self.current_history_index):
            self.current_history_index+=1
        else:
            raise IndexError

    def add_new_key_to_history(self,key)->np.ndarray:
        if self.current_history_index<len(self.current_history_index)-1:
            while(self.current_history_index<len(self.current_history_index)-1):
                self.history.pop(len(self.current_history_index)-1)
        self.history.append(key)

    def reset(self)->np.ndarray:
        zero_key = self.history[0]
        self.add_new_key_to_history(zero_key)
        splited_key  = zero_key.split('|')
        self.values[EffectType.STRAIGHTENED.value] = ("True"==splited_key[1])
        self.values[EffectType.CONTRAST_INTENSITY.value] = float(splited_key[2])
        self.values[EffectType.UPPER_SHIFT.value] = float(splited_key[3])
        self.values[EffectType.LOWER_SHIFT.value] = float(splited_key[4])



