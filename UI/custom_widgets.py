from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QCheckBox, QComboBox, QSlider, QSizePolicy, QGroupBox)
from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtGui import QDrag, QFont, QColor, QPainter

import random

class CustomCheckBoxWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(5)  # Add some spacing between label and checkbox

        self.label = QLabel(text)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure the label has no background and correct text color
        self.checkbox = QCheckBox()

        self.layout.addWidget(self.label)
        self.layout.addStretch()  # Add stretch to push the checkbox to the right
        self.layout.addWidget(self.checkbox)

        self.setLayout(self.layout)

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)

    def isChecked(self):
        return self.checkbox.isChecked()

    def connect(self, callback):
        self.checkbox.stateChanged.connect(callback)

    def setStyleSheet(self, style):
        self.checkbox.setStyleSheet(style)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure label style is applied correctly

class CustomComboBoxWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(5)  # Add some spacing between label and combobox

        self.label = QLabel(text)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure the label has no background and correct text color
        self.combobox = QComboBox()

        self.layout.addWidget(self.label)
        self.layout.addStretch()  # Add stretch to push the combobox to the right
        self.layout.addWidget(self.combobox)

        self.setLayout(self.layout)

    def addItems(self, items):
        self.combobox.addItems(items)

    def setStyleSheet(self, style):
        self.combobox.setStyleSheet(style)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure label style is applied correctly

class CustomSliderWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(5)  # Add some spacing between label and slider

        self.label = QLabel(text)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure the label has no background and correct text color
        self.slider = CustomSlider(Qt.Horizontal)
        self.slider.setRange(1, 250)
        self.slider.setValue(1)  # Set the default value to 1
        self.slider.valueChanged.connect(self.update_label)

        self.layout.addWidget(self.label)
        self.layout.addStretch()  # Add stretch to push the slider to the right
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

        self.update_label(1)  # Update the label to show the initial value

    def setRange(self, min_val, max_val):
        self.slider.setRange(min_val, max_val)

    def value(self):
        return self.slider.value()

    def connect(self, callback):
        self.slider.valueChanged.connect(callback)

    def setStyleSheet(self, style):
        self.slider.setStyleSheet(style)
        self.label.setStyleSheet("background-color: transparent; color: #FFFFFF;")  # Ensure label style is applied correctly

    def update_label(self, value):
        self.label.setText(f"{value} Compression Repeats")

class CustomSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            value = self.minimum() + (self.maximum() - self.minimum()) * x / self.width()
            self.setValue(int(value))
        super().mousePressEvent(event)

class DraggableGroupBox(QGroupBox):
    def __init__(self, title, parent_gui, parent=None):
        super().__init__(title, parent)
        self.parent_gui = parent_gui
        self.setAcceptDrops(True)
        self.setStyleSheet("QGroupBox { background-color: #1E1A3D; border: 1px solid #777; border-radius: 4px; }")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            drag.setMimeData(mime_data)
            drag.setHotSpot(event.pos())
            drop_action = drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.source().parentWidget() == self.parentWidget():
            event.acceptProposedAction()

    def dropEvent(self, event):
        source = event.source()
        if source and source.parentWidget() == self.parentWidget():
            self.parent_gui.swap_groupboxes(source, self)
            event.acceptProposedAction()
            
class GlitchLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Montserrat', 20, QFont.Bold))
        self.setStyleSheet("color: white;")
        self.setText(text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_glitch)
        self.timer.start(16)  # Faster timer for smoother updates (~60 FPS)

        self.current_offset = (0, 0)
        self.target_offset = (0, 0)
        self.lerp_speed = 0.65  # Faster interpolation speed for noticeable movement
        self.colors = [QColor(251, 13, 67), QColor(82, 0, 189)]  # red and purple
        self.update_frequency = 10  # More frequent updates to the target offset
        self.update_counter = 0

    def update_glitch(self):
        self.update_counter += 1
        if self.update_counter >= self.update_frequency:
            self.update_counter = 0
            # Update the target offset to create a new glitch effect, ensuring it's not zero
            while True:
                new_target_offset = (random.randint(-2, 2), random.randint(-2, 2))
                if new_target_offset != (0, 0):
                    self.target_offset = new_target_offset
                    break

        # Linearly interpolate the current offset towards the target offset
        self.current_offset = (
            self.lerp(self.current_offset[0], self.target_offset[0], self.lerp_speed),
            self.lerp(self.current_offset[1], self.target_offset[1], self.lerp_speed)
        )

        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font())

        # Draw glitch effect with interpolated offsets, ensuring the offsets are non-zero
        for color, offset_multiplier in zip(self.colors, [1, -1]):
            x = int(self.current_offset[0] * offset_multiplier)
            y = int(self.current_offset[1] * offset_multiplier)
            if x == 0 and y == 0:
                continue
            painter.setPen(color)
            painter.drawText(x, y, self.width(), self.height(), Qt.AlignCenter, self.text())

        # Draw the main text in white
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(0, 0, self.width(), self.height(), Qt.AlignCenter, self.text())

    @staticmethod
    def lerp(start, end, t):
        return start + t * (end - start)