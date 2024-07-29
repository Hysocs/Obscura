import sys
import logging
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, 
                             QCheckBox, QTextEdit, QHBoxLayout, QStackedWidget, QFrame, QGroupBox, QLineEdit, QComboBox, QGridLayout, QSpacerItem, QSizePolicy, QSlider)
from PyQt5.QtCore import Qt, QPoint, QSize, QMetaObject, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QFont, QPainter, QDrag, QCursor
from Core.obfuscator import CodeObfuscator
import random

from UI.custom_widgets import CustomCheckBoxWidget, CustomComboBoxWidget, CustomSliderWidget, CustomSlider, DraggableGroupBox, GlitchLabel

class QTextEditLogger(logging.Handler, QObject):
    append_text_signal = pyqtSignal(str)

    def __init__(self, text_edit):
        super().__init__()
        QObject.__init__(self)
        self.text_edit = text_edit
        self.append_text_signal.connect(self.append_text)

    def emit(self, record):
        msg = self.format(record)
        self.append_text_signal.emit(msg)

    def append_text(self, msg):
        self.text_edit.append(msg)

class TitleBar(QFrame):
    def __init__(self, parent, obfuscator_btn_callback, settings_btn_callback):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #181534; border: none;")

        self.parent = parent
        self.maxNormal = False

        self.title = GlitchLabel("Obscura", self)
        self.title.setContentsMargins(15, 0, 0, 0)

        self.obfuscator_btn = QPushButton('📄 File Obfuscator', self)
        self.obfuscator_btn.setStyleSheet("background-color: #181534; color: #FFFFFF; padding: 10px 20px; font-size: 16px;")
        self.obfuscator_btn.clicked.connect(obfuscator_btn_callback)

        self.settings_btn = QPushButton('📂 Project Obfuscator', self)
        self.settings_btn.setStyleSheet("background-color: #181534; color: #FFFFFF; padding: 10px 20px; font-size: 16px;")
        self.settings_btn.clicked.connect(settings_btn_callback)

        self.minimizeButton = QPushButton('-', self)
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.setStyleSheet("background-color: #181534; color: #FFFFFF; border: none;")
        self.minimizeButton.clicked.connect(self.parent.showMinimized)
        
        self.maximizeButton = QPushButton('□', self)
        self.maximizeButton.setFixedSize(30, 30)
        self.maximizeButton.setStyleSheet("background-color: #181534; color: #FFFFFF; border: none;")
        self.maximizeButton.clicked.connect(self.maximize_restore)
        
        self.closeButton = QPushButton('x', self)
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet("background-color: #181534; color: #FFFFFF; border: none;")
        self.closeButton.clicked.connect(self.parent.close)
        
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.title)
        
        self.hbox.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        
        self.hbox.addWidget(self.obfuscator_btn)
        self.hbox.addWidget(self.settings_btn)
        self.hbox.addStretch()
        self.hbox.addWidget(self.minimizeButton)
        self.hbox.addWidget(self.maximizeButton)
        self.hbox.addWidget(self.closeButton)
        self.hbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox)

        self.start = QPoint(0, 0)
        self.pressing = False

    def maximize_restore(self):
        if self.maxNormal:
            self.parent.showNormal()
            self.maxNormal = False
            self.maximizeButton.setText('□')
        else:
            self.parent.showMaximized()
            self.maxNormal = True
            self.maximizeButton.setText('❐')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.parent.move(self.parent.pos() + event.globalPos() - self.start)
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressing = False

class ObfuscatorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #110F25; color: #FFFFFF;")  # Darkened Super Dark Blue Background with White Text

        self.file_path = 'C:\\Users\\Administrator\\Desktop\\Testers\\DancingLinks.py'
        self.init_ui()
        self.setup_logging()

        # Highlight the obfuscator tab by default
        self.show_obfuscator()

        self.oldPos = self.pos()
        self.resizing = False

    def get_custom_checkbox_style(self):
        with open("UI/checkboxes.qss", "r") as f:
            return f.read()
        
    def get_custom_groupbox_style(self):
        with open("UI/groupboxes.qss", "r") as f:
            return f.read()
        
    def get_custom_combobox_style(self):
        with open("UI/dropdown.qss", "r") as f:
            return f.read()
        
    def get_custom_slider_style(self):
        with open("UI/slider.qss", "r") as f:
            return f.read()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = TitleBar(self, self.show_obfuscator, self.show_settings)
        main_layout.addWidget(self.title_bar)

        self.stack = QStackedWidget(self)
        self.obfuscator_widget = QWidget()
        self.settings_widget = QWidget()

        self.stack.addWidget(self.obfuscator_widget)
        self.stack.addWidget(self.settings_widget)

        main_layout.addWidget(self.stack)

        # Add resize handle
        self.resize_handle = QLabel(self)
        self.resize_handle.setFixedSize(22, 22)
        self.resize_handle.setStyleSheet("background-color: transparent; image: url('UI/resize.png');")
        self.resize_handle.setCursor(QCursor(Qt.SizeFDiagCursor))

        self.init_obfuscator_ui()
        self.init_settings_ui()
        
        self.setLayout(main_layout)
        self.setWindowTitle('Code Obfuscator')
        self.resize(800, 600)
    
    def resizeEvent(self, event):
        self.resize_handle.move(self.width() - 16, self.height() - 16)
        super().resizeEvent(event)
    
    def init_obfuscator_ui(self):
        layout = QGridLayout(self.obfuscator_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.group_boxes = []

        # Group for obfuscate identifiers
        identifiers_group = DraggableGroupBox("Obfuscation Settings", self)
        identifiers_group.setMaximumWidth(380)  # Set the maximum width for the group
        obfuscation_layout = QVBoxLayout()
        obfuscation_layout.setAlignment(Qt.AlignTop)
        obfuscation_layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Add this after the existing obfuscation settings checkboxes
        self.function_mirroring_cb = CustomCheckBoxWidget('Function Mirroring')
        self.function_mirroring_cb.setChecked(True)
        self.function_mirroring_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.function_mirroring_cb)

        self.inline_code_replacement_cb = CustomCheckBoxWidget('Inline Code Obfuscation')
        self.inline_code_replacement_cb.setChecked(True)
        self.inline_code_replacement_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.inline_code_replacement_cb)

        self.control_flow_obfuscation_cb = CustomCheckBoxWidget('Control Flow Obfuscation')
        self.control_flow_obfuscation_cb.setChecked(True)
        self.control_flow_obfuscation_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.control_flow_obfuscation_cb)

        self.control_flow_flatten_obfuscation_cb = CustomCheckBoxWidget('Control Flow Flatten Obfuscation')
        self.control_flow_flatten_obfuscation_cb.setChecked(True)
        self.control_flow_flatten_obfuscation_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.control_flow_flatten_obfuscation_cb)

        self.obfuscate_identifiers_cb = CustomCheckBoxWidget('Obfuscate Identifiers (Functions, Classes, Variables)')
        self.obfuscate_identifiers_cb.setChecked(True)
        self.obfuscate_identifiers_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.obfuscate_identifiers_cb)

        # Existing group for obfuscate constants
        self.obfuscate_constants_cb = CustomCheckBoxWidget('Obfuscate Constants')
        self.obfuscate_constants_cb.setChecked(True)
        self.obfuscate_constants_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.obfuscate_constants_cb)

        self.number_to_hex_cb = CustomCheckBoxWidget('Convert Numbers to Hex')
        self.number_to_hex_cb.setChecked(True)
        self.number_to_hex_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.number_to_hex_cb)

        # Add Opaque Predicates checkbox
        self.opaque_predicates_cb = CustomCheckBoxWidget('Opaque Predicates')
        self.opaque_predicates_cb.setChecked(True)
        self.opaque_predicates_cb.setStyleSheet(self.get_custom_checkbox_style())
        obfuscation_layout.addWidget(self.opaque_predicates_cb)

        identifiers_group.setLayout(obfuscation_layout)
        identifiers_group.setStyleSheet(self.get_custom_groupbox_style())
        layout.addWidget(identifiers_group, 0, 0)
        self.group_boxes.append(identifiers_group)

        # Group for encryption settings
        encryption_group = DraggableGroupBox("Encryption Settings", self)
        encryption_group.setMaximumWidth(380)  # Set the maximum width for the group
        encryption_layout = QVBoxLayout()
        encryption_layout.setAlignment(Qt.AlignTop)

        # Add a spacer item to create space at the top
        encryption_layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.encrypt_code_cb = CustomCheckBoxWidget('Encrypt Code')
        self.encrypt_code_cb.setChecked(False)
        self.encrypt_code_cb.setStyleSheet(self.get_custom_checkbox_style())
        self.encrypt_code_cb.connect(self.toggle_encrypt_group)
        encryption_layout.addWidget(self.encrypt_code_cb)

        self.encrypt_method_cb = CustomComboBoxWidget('Encryption Method')
        self.encrypt_method_cb.addItems([ "Hybrid Hash (Custom Method)", "AES (Requires pycryptodome)", "Base64 (Default Python)", "Hybrid (Anti-V)"])
        self.encrypt_method_cb.setStyleSheet(self.get_custom_combobox_style())
        self.encrypt_method_cb.setVisible(False)  # Initially hide the combobox
        encryption_layout.addWidget(self.encrypt_method_cb)

        self.encrypt_group = DraggableGroupBox("Additional Encryption Settings", self)
        self.encrypt_group_layout = QVBoxLayout()
        self.encrypt_group_layout.setAlignment(Qt.AlignTop)

        # Add a spacer item to create space at the top
        self.encrypt_group_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.inject_anti_debug_cb = CustomCheckBoxWidget('Inject Anti-Debug')
        self.inject_anti_debug_cb.setChecked(False)
        self.inject_anti_debug_cb.setStyleSheet(self.get_custom_checkbox_style())
        self.encrypt_group_layout.addWidget(self.inject_anti_debug_cb)

        self.obfuscate_decryption_stub_cb = CustomCheckBoxWidget('Re-Obfuscate Encrypted Code (Obfuscates Decryption Stub)')
        self.obfuscate_decryption_stub_cb.setChecked(True)
        self.obfuscate_decryption_stub_cb.setStyleSheet(self.get_custom_checkbox_style())
        self.encrypt_group_layout.addWidget(self.obfuscate_decryption_stub_cb)

        self.encrypt_group.setLayout(self.encrypt_group_layout)
        self.encrypt_group.setVisible(False)
        encryption_layout.addWidget(self.encrypt_group)

        encryption_group.setLayout(encryption_layout)
        encryption_group.setStyleSheet(self.get_custom_groupbox_style())
        layout.addWidget(encryption_group, 0, 1)
        self.group_boxes.append(encryption_group)

        # Group for insert dummy code
        dummy_code_group = DraggableGroupBox("Dummy Code Settings", self)
        dummy_code_group.setMaximumWidth(380)  # Set the maximum width for the group
        dummy_code_layout = QVBoxLayout()
        dummy_code_layout.setAlignment(Qt.AlignTop)
        
        # Add a spacer item to create space at the top
        dummy_code_layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.insert_dummy_cb = CustomCheckBoxWidget('Insert Dummy Variables & Args')
        self.insert_dummy_cb.setChecked(True)
        self.insert_dummy_cb.setStyleSheet(self.get_custom_checkbox_style())
        dummy_code_layout.addWidget(self.insert_dummy_cb)

        dummy_code_group.setLayout(dummy_code_layout)
        dummy_code_group.setStyleSheet(self.get_custom_groupbox_style())
        layout.addWidget(dummy_code_group, 1, 0)
        self.group_boxes.append(dummy_code_group)

        # Group for compress code settings
        compress_code_group = DraggableGroupBox("Compress Code Settings", self)
        compress_code_group.setMaximumWidth(380)  # Set the maximum width for the group
        compress_code_layout = QVBoxLayout()
        compress_code_layout.setAlignment(Qt.AlignTop)
        
        # Add a spacer item to create space at the top
        compress_code_layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.compress_code_cb = CustomCheckBoxWidget('Compress Code')
        self.compress_code_cb.setChecked(False)
        self.compress_code_cb.setStyleSheet(self.get_custom_checkbox_style())
        self.compress_code_cb.connect(self.toggle_compress_repeat_options)
        compress_code_layout.addWidget(self.compress_code_cb)

        self.compress_repeat_slider = CustomSliderWidget('Compression Repeats')
        self.compress_repeat_slider.setStyleSheet(self.get_custom_slider_style())
        self.compress_repeat_slider.setVisible(False)
        compress_code_layout.addWidget(self.compress_repeat_slider)

        compress_code_group.setLayout(compress_code_layout)
        compress_code_group.setStyleSheet(self.get_custom_groupbox_style())
        layout.addWidget(compress_code_group, 1, 1)
        self.group_boxes.append(compress_code_group)

        # Console
        console_group = QGroupBox("Console Output")
        console_group.setStyleSheet(self.get_custom_groupbox_style())

        console_layout = QVBoxLayout()
        console_layout.setContentsMargins(0, 10, 0, 0)  # Remove margins
        console_layout.setSpacing(0)  # Remove spacing

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            background-color: #191735; 
            color: #FFFFFF; 
            border: none; /* Remove border from QTextEdit as it is inside QGroupBox */
        """)
        console_layout.addWidget(self.log_output)
        console_group.setLayout(console_layout)

        layout.addWidget(console_group, 2, 0, 1, 2)

        # Group for file selection and obfuscate button
        file_group = QGroupBox("File Settings")
        file_layout = QVBoxLayout()
        file_layout.setAlignment(Qt.AlignTop)

        # Add a spacer item to create space at the top
        file_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.label = QLabel(f"Selected file: {self.file_path}")
        file_layout.addWidget(self.label)

        self.select_file_btn = QPushButton('Select File')
        self.select_file_btn.setStyleSheet("background-color: #1E1A3D; color: #FFFFFF;")
        self.select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_file_btn)

        self.obfuscate_btn = QPushButton('Obfuscate')
        self.obfuscate_btn.setStyleSheet("background-color: #1E1A3D; color: #FFFFFF;")
        self.obfuscate_btn.clicked.connect(self.obfuscate)
        file_layout.addWidget(self.obfuscate_btn)

        file_group.setLayout(file_layout)
        file_group.setStyleSheet(self.get_custom_groupbox_style())
        layout.addWidget(file_group, 3, 0, 1, 2)

        self.obfuscator_widget.setLayout(layout)

    def swap_groupboxes(self, source, target):
        layout = self.obfuscator_widget.layout()
        
        # Find the positions of the source and target widgets in the grid layout
        source_index = layout.indexOf(source)
        target_index = layout.indexOf(target)
        
        if source_index != -1 and target_index != -1:
            source_item = layout.itemAt(source_index)
            target_item = layout.itemAt(target_index)
            
            source_pos = layout.getItemPosition(source_index)
            target_pos = layout.getItemPosition(target_index)
            
            # Remove the widgets from their current positions
            layout.removeWidget(source)
            layout.removeWidget(target)
            
            # Add the widgets back at each other's positions
            layout.addWidget(target, *source_pos[:2])
            layout.addWidget(source, *target_pos[:2])

        self.obfuscator_widget.update()

    def toggle_encrypt_group(self, state):
        self.encrypt_group.setVisible(state == Qt.Checked)
        self.encrypt_method_cb.setVisible(state == Qt.Checked)

    def toggle_compress_repeat_options(self, state):
        self.compress_repeat_slider.setVisible(state == Qt.Checked)

    def init_settings_ui(self):
        layout = QVBoxLayout(self.settings_widget)
        self.settings_label = QLabel("Project Obfuscator 'will allow you to select a folder and it will be able to obfuscate all .py files and not break cross referencing, etc' (to be implemented)")
        self.settings_label.setStyleSheet("color: #FFFFFF;")  # Ensure visibility
        layout.addWidget(self.settings_label)

    def setup_logging(self):
        text_edit_logger = QTextEditLogger(self.log_output)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_edit_logger.setFormatter(formatter)
        logger = logging.getLogger()
        if not any(isinstance(handler, QTextEditLogger) for handler in logger.handlers):
            logger.addHandler(text_edit_logger)
        logger.setLevel(logging.INFO)

    def show_obfuscator(self):
        self.title_bar.obfuscator_btn.setStyleSheet("background-color: #1E1A3B; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 13px;")  # Brighter when active
        self.title_bar.settings_btn.setStyleSheet("background-color: #181534; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 13px;")
        self.stack.setCurrentWidget(self.obfuscator_widget)

    def show_settings(self):
        self.title_bar.settings_btn.setStyleSheet("background-color: #1E1A3B; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 13px;")  # Brighter when active
        self.title_bar.obfuscator_btn.setStyleSheet("background-color: #181534; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 13px;")
        self.stack.setCurrentWidget(self.settings_widget)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Obfuscate", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Selected file: {self.file_path}")

    # Modify the obfuscate method in your GUI
    def obfuscate(self):
        options = {
            "inline_code_replacement": self.inline_code_replacement_cb.isChecked(),
            "control_flow_obfuscation": self.control_flow_obfuscation_cb.isChecked(),
            "control_flow_flatten_obfuscation": self.control_flow_flatten_obfuscation_cb.isChecked(),
            "obfuscate_identifiers": self.obfuscate_identifiers_cb.isChecked(),
            "obfuscate_constants": self.obfuscate_constants_cb.isChecked(),
            "encrypt_code": self.encrypt_code_cb.isChecked(),
            "encryption_method": self.encrypt_method_cb.combobox.currentText() if self.encrypt_code_cb.isChecked() else None,
            "obfuscate_decryption_stub": self.obfuscate_decryption_stub_cb.isChecked(),
            "inject_anti_debug": self.inject_anti_debug_cb.isChecked(),
            "compress_code_flag": self.compress_code_cb.isChecked(),
            "repeat_count": self.compress_repeat_slider.value() if self.compress_code_cb.isChecked() else 1,
            "function_mirroring": self.function_mirroring_cb.isChecked(),
            "number_to_hex": self.number_to_hex_cb.isChecked(),
            "opaque_predicates": self.opaque_predicates_cb.isChecked(),  # Add this line
            "insert_dummy_variables": self.insert_dummy_cb.isChecked(),  # Add this line
        }

        # Log the options dictionary
        logging.info(f"Obfuscation options: {options}")

        new_file_path = CodeObfuscator.obfuscate_file(self.file_path, options)

        if new_file_path:
            self.label.setText(f"Obfuscated file written to: {new_file_path}")
        else:
            self.label.setText("Failed to obfuscate the file.")



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            self.resizing = event.pos().x() > self.width() - 16 and event.pos().y() > self.height() - 16
            self.oldSize = self.size()

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPos() - self.oldPos
            new_width = self.oldSize.width() + delta.x()
            new_height = self.oldSize.height() + delta.y()
            self.resize(QSize(new_width, new_height))
        else:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.resizing = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ObfuscatorGUI()
    gui.show()
    sys.exit(app.exec_())