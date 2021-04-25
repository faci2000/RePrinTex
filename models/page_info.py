class PageInfo:
    def __init__(self) -> None:
        self.text_lines = []
        self.letters = {}
        upuppers = []
        lolowers = []
        uppers = []
        lowers = []
        self.lines = {"upuppers":upuppers,"lolowers":lolowers,"uppers":uppers,"lowers":lowers}
        self.text_block={"x":0,"y":0,"w":0,"h":0}