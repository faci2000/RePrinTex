from models.effects import EffectType
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton


def add_clean(parent, widget, layout):
    l1 = QLabel("Cleaning parameters")
    l2 = QLabel("Light")
    l3 = QLabel("Dark")

    parent.clean_slider_light = create_slider(-50, 50, 0)
    parent.clean_slider_dark = create_slider(40, 80, 50)
    widget.clean_button = create_button(widget, "Clean page")

    layout.addWidget(l1)
    layout.addWidget(l2)
    layout.addWidget(parent.clean_slider_light)
    layout.addWidget(l3)
    layout.addWidget(parent.clean_slider_dark)
    layout.addWidget(widget.clean_button)

    widget.clean_button.clicked.connect(
        lambda: parent.controller.change_effects({'effect_type':EffectType.LOWER_SHIFT,'org':False,
                                                    'values':[{'type':EffectType.LOWER_SHIFT, 'value':parent.clean_slider_dark.value()},
                                                            {'type':EffectType.UPPER_SHIFT, 'value':parent.clean_slider_light.value()},
                                                            {'type':EffectType.CONTRAST_INTENSITY, 'value':parent.contrast_slider.value()* 1.0 / 10}]}))

def add_contrast(parent, widget, layout):
    l1 = QLabel("Contrast parameters")
    l2 = QLabel("Contrast intensity")

    parent.contrast_slider = create_slider(1, 30, 10)
    widget.contrast_button = create_button(widget, "Change contrast")

    layout.addWidget(l1)
    layout.addWidget(l2)
    layout.addWidget(parent.contrast_slider)
    layout.addWidget(widget.contrast_button)

    widget.contrast_button.clicked.connect(lambda: setattr(parent.controller.modified_effects, "contrast_intensity",
                                                         parent.contrast_slider.value() * 1.0 / 10))
    widget.contrast_button.clicked.connect(lambda: parent.controller.contrast())


def add_stains(parent, widget, layout):
    widget.stains_button = create_button(widget, "Removing stains", True)
    parent.stains_slider = create_slider(1, 100, 20)
    l1 = QLabel("Remove Stains")
    l2 = QLabel("Brush size")

    layout.addWidget(l1)
    layout.addWidget(l2)
    layout.addWidget(parent.stains_slider)
    layout.addWidget(widget.stains_button)


def create_slider(min_, max_, initial):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_)
    slider.setMaximum(max_)
    slider.setValue(initial)
    return slider


def create_button(widget, text, check=False):
    button = QPushButton(widget)
    button.setText(text)
    if check:
        button.setCheckable(True)
    return button
