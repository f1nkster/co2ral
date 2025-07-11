from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider


class LabelValueSlider(QHBoxLayout):
    def __init__(self, name: str, min_value: int, max_value: int, value: int, unit: str = "") -> None:
        super().__init__()

        self.unit = unit

        self.sl = QSlider(orientation=Qt.Orientation.Horizontal)
        self.sl.setMinimum(min_value)
        self.sl.setMaximum(max_value)
        # self.sl.setMaximumWidth(50)
        self.sl.setValue(value)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)

        self.label_name = QLabel(name)
        self.label_name.setAlignment(Qt.AlignCenter)

        self.label_value = QLabel(f"{value} {self.unit}")
        self.label_value.setAlignment(Qt.AlignCenter)

        self.addWidget(self.label_name)
        self.addWidget(self.sl)
        self.addWidget(self.label_value)

    def set_text(self, text: str) -> None:
        """Sets the text.

        :param text: Text
        """
        self.label_value.setText(f"{text} {self.unit}")
