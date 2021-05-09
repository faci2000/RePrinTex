from services.images_provider import ImagesProvider
from models.effects import EffectType, Lines
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QDockWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QWidget, QPushButton

from controllers.guielements.effects_controller import EffectsController


class EffectsView:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.controller:EffectsController = EffectsController(parent, self)
        self.dock = QDockWidget("Effects", self.parent)
        self.widget = QWidget(self.dock)
        ImagesProvider().effects_view=self

        layout = QVBoxLayout(self.widget)
        layout.setAlignment(Qt.AlignTop)

        # Sliders
        self.clean_slider_light = create_slider(-50, 50, 0)
        self.clean_slider_dark = create_slider(40, 80, 50)
        self.contrast_slider = create_slider(1, 30, 10)
        self.stains_slider = create_slider(1, 100, 20)

        # Buttons
        # self.straighten_button = self.create_button("Straighten lines", self.controller.straighten_lines)
        self.clean_button = self.create_button("Clean page")
        self.contrast_button = self.create_button("Change contrast")
        self.stains_button = self.create_button("Removing stains", None, True)
        self.apply_button = self.create_button("Apply", lambda: self.controller.apply())
        self.apply_all_button = self.create_button("Apply to all", lambda: self.controller.apply_all())
        self.reset_button = self.create_button("Reset", lambda: self.controller.reset())
        # self.clean_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"upper_shift",self.clean_slider_light.value()))
        # self.clean_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"lower_shift",self.clean_slider_dark.value()))
        # self.clean_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"contrast_intensity",self.contrast_slider.value()* 1.0 / 10))

        self.clean_button.clicked.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LOWER_SHIFT,'org':False,
                                                                                  'values':[{'type':EffectType.LOWER_SHIFT, 'value':self.clean_slider_dark.value()},
                                                                                            {'type':EffectType.UPPER_SHIFT, 'value':self.clean_slider_light.value()},
                                                                                            {'type':EffectType.CONTRAST_INTENSITY, 'value':self.contrast_slider.value()* 1.0 / 10}]}))

        self.contrast_button.clicked.connect(lambda: self.controller.change_effects({'effect_type':EffectType.CONTRAST_INTENSITY,'org':False,
                                                                                  'values':[{'type':EffectType.LOWER_SHIFT, 'value':self.clean_slider_dark.value()},
                                                                                            {'type':EffectType.UPPER_SHIFT, 'value':self.clean_slider_light.value()},
                                                                                            {'type':EffectType.CONTRAST_INTENSITY, 'value':self.contrast_slider.value()* 1.0 / 10}]}))
        # self.contrast_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"upper_shift",self.clean_slider_light.value()))
        # self.contrast_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"lower_shift",self.clean_slider_dark.value()))
        # self.contrast_button.clicked.connect(lambda: setattr(self.controller.modified_effects,"contrast_intensity",self.contrast_slider.value()* 1.0 / 10))
        # self.contrast_button.clicked.connect(lambda: self.controller.updated_drawing_effects(True))

        self.add_to_layout(layout)

        self.dock.setWidget(self.widget)
        self.widget.setLayout(layout)

    def add_to_layout(self, layout:QVBoxLayout):
        # Labels
        l1 = QLabel("Cleaning parameters")
        l2 = QLabel("Light")
        l3 = QLabel("Dark")
        l4 = QLabel("Contrast parameters")
        l5 = QLabel("Contrast intensity")
        l6 = QLabel("Stain remover brush size")

        # Clean
        layout.addWidget(l1)
        layout.addWidget(l2)
        layout.addWidget(self.clean_slider_light)
        layout.addWidget(l3)
        layout.addWidget(self.clean_slider_dark)
        layout.addWidget(self.clean_button)

        # Contrast
        layout.addWidget(l4)
        layout.addWidget(l5)
        layout.addWidget(self.contrast_slider)
        layout.addWidget(self.contrast_button)

        # Stains
        layout.addWidget(l6)
        layout.addWidget(self.stains_slider)
        layout.addWidget(self.stains_button)

        # Control
        layout.addWidget(self.apply_button)
        layout.addWidget(self.apply_all_button)
        layout.addWidget(self.reset_button)

        #Checkboxes - lines control
        layout.addLayout(self.create_checkobxes())

    def get_view(self):
        return self.dock

    def create_button(self, text, controller=None, check=False):
        button = QPushButton(self.widget)
        button.setText(text)
        if controller:
            button.clicked.connect(controller)
        if check:
            button.setCheckable(True)
        return button

    def create_checkobxes(self):
        # labels = [" ","Main lines","Minor lines","Text block","Words","Letters"]
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(' '))
        for label in Lines:
            vbox.addWidget(QLabel(label.value))
        hbox.addLayout(vbox)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Original"))

        # for label in Lines:
        #     label_str = label.value[:]
        #     print(label_str)
        #     chk = QCheckBox()
        #     chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':label_str,'org':True,'value':not chk.isChecked()}))
        #     vbox.addWidget(chk)
        # hbox.addLayout(vbox)

        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.MAIN_LINES.value,'org':True}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.MINOR_LINES.value,'org':True}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.TEXT_BLOCK.value,'org':True}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.WORDS.value,'org':True}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.LETTERS.value,'org':True}))
        vbox.addWidget(chk)
        hbox.addLayout(vbox)



        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Preview"))
        # x=[val.value for val in Lines]
        # print(x)
        # for i in range(len(x)):
        #     chk = QCheckBox()
        #     chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':x[i],'org':False,'value':not chk.isChecked()}))
        #     vbox.addWidget(chk)
        # hbox.addLayout(vbox)

        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.MAIN_LINES.value,'org':False}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.MINOR_LINES.value,'org':False}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.TEXT_BLOCK.value,'org':False}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.WORDS.value,'org':False}))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: self.controller.change_effects({'effect_type':EffectType.LINES,'type':Lines.LETTERS.value,'org':False}))
        vbox.addWidget(chk)
        hbox.addLayout(vbox)

        # print("returnig vbox")
        return hbox


def create_slider(min_, max_, initial):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_)
    slider.setMaximum(max_)
    slider.setValue(initial)
    return slider



