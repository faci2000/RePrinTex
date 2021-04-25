from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QSlider, QLabel, QWidget, QPushButton

from controllers.guielements.effects_controller import EffectsController


class EffectsView:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.controller = EffectsController(parent, self)
        self.dock = QDockWidget("Effects", self.parent)
        self.widget = QWidget(self.dock)

        layout = QVBoxLayout(self.widget)
        layout.setAlignment(Qt.AlignTop)

        # Buttons
        # self.straighten_button = self.create_button("Straighten lines", self.controller.straighten_lines)
        self.clean_button = self.create_button("Clean page", lambda: self.controller.clean())
        self.contrast_button = self.create_button("Change contrast", lambda: self.controller.contrast())
        self.stains_button = self.create_button("Removing stains", None, True)
        self.apply_button = self.create_button("Apply", lambda: self.controller.apply())
        self.apply_all_button = self.create_button("Apply to all", lambda: self.controller.apply_all())
        self.reset_button = self.create_button("Reset", lambda: self.controller.reset())

        # Sliders
        self.clean_slider_light = create_slider(-50, 50, 0)
        self.clean_slider_dark = create_slider(40, 80, 50)
        self.contrast_slider = create_slider(1, 30, 10)
        self.stains_slider = create_slider(1, 100, 20)

        self.add_to_layout(layout)

        self.dock.setWidget(self.widget)
        self.widget.setLayout(layout)

    def add_to_layout(self, layout):
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

    def get_view(self):
        return self.dock

    def create_button(self, text, controller, check=False):
        button = QPushButton(self.widget)
        button.setText(text)
        if controller:
            button.clicked.connect(controller)
        if check:
            button.setCheckable(True)
        return button


def create_slider(min_, max_, initial):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_)
    slider.setMaximum(max_)
    slider.setValue(initial)
    return slider
