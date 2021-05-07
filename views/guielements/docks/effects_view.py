from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QDockWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QWidget, QPushButton

from controllers.guielements.effects_controller import EffectsController
from views.guielements.effects_layout import add_clean, add_stains, add_contrast


class EffectsView:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.controller:EffectsController = EffectsController(parent, self)
        self.dock = QDockWidget("Effects", self.parent)
        self.widget = QWidget(self.dock)

        layout = QVBoxLayout(self.widget)
        layout.setAlignment(Qt.AlignTop)

        self.apply_button = self.create_button("Apply", lambda: self.controller.apply())
        self.apply_all_button = self.create_button("Apply to all", lambda: self.controller.apply_all())
        self.reset_button = self.create_button("Reset", lambda: self.controller.reset())
        self.add_to_layout(layout)

        self.dock.setWidget(self.widget)
        self.widget.setLayout(layout)

    def add_to_layout(self, layout:QVBoxLayout):
        add_clean(self, self.widget, layout)
        add_contrast(self, self.widget, layout)
        add_stains(self, self.widget, layout)

        # Control
        layout.addWidget(self.apply_button)
        layout.addWidget(self.apply_all_button)
        layout.addWidget(self.reset_button)

        # Checkboxes - lines control
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
        labels = [" ","Main lines","Minor lines","Text block","Words","Letters"]
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        for label in labels:
            vbox.addWidget(QLabel(label))
        hbox.addLayout(vbox)
        
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Original"))
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"main_lines",not self.controller.original_effects.main_lines))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(True))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"minor_lines",not self.controller.original_effects.minor_lines))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(True))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"text_block",not self.controller.original_effects.text_block))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(True))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"words",not self.controller.original_effects.words))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(True))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"letters",not self.controller.original_effects.letters))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(True))
        vbox.addWidget(chk)
        hbox.addLayout(vbox)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Preview"))
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.modified_effects,"main_lines",not self.controller.modified_effects.main_lines))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(False))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"minor_lines",not self.controller.modified_effects.minor_lines))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(False))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"text_block",not self.controller.modified_effects.text_block))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(False))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"words",not self.controller.modified_effects.words))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(False))
        vbox.addWidget(chk)
        chk = QCheckBox()
        chk.stateChanged.connect(lambda: setattr(self.controller.original_effects,"letters",not self.controller.modified_effects.letters))
        chk.stateChanged.connect(lambda: self.controller.updated_drawing_effects(False))
        vbox.addWidget(chk)
        hbox.addLayout(vbox)

        print("returnig vbox")
        return hbox


def create_slider(min_, max_, initial):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_)
    slider.setMaximum(max_)
    slider.setValue(initial)
    return slider



