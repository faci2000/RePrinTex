

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
        self.values[EffectType.LINES]={}
        self.values[EffectType.UPPER_SHIFT]=0
        self.values[EffectType.LOWER_SHIFT]=0
        self.values[EffectType.CONTRAST_INTENSITY]=0
        self.values[EffectType.STRAIGHTENED]=False
        self.values[EffectType.CORRECTIONS]={}
        self.current_history_index = 0
        self.history = []
        self.reworked_imgs = {}

    def get_key(self, img_path):
        return (img_path + str(self.values[EffectType.STRAIGHTENED]) + str(self.values[EffectType.CONTRAST_INTENSITY]) +
                str(self.values[EffectType.UPPER_SHIFT]) + str(self.values[EffectType.LOWER_SHIFT]) +
                str(self.values[EffectType.CORRECTIONS]))
        


