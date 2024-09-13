# Class created by MateiObrocea

import os, sys, platform
from PyQt5 import QtCore, QtWidgets


# ----- Imports of the other classes -------------------------------------------
from graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider
from preview_window import PreviewWindow
from camera_controls import CameraControls
from arduino_controller import ArduinoController
from hover_button import HoverButton
from protocol_constants import MOVE_STAGE_UP, MOVE_STAGE_DOWN, MOVE_STAGE_LEFT, MOVE_STAGE_RIGHT, STAGE_STOP, RTI_RESET
from led_button_controller import LedButtonController

# ----- Camera imports ---------------------------------------------------------

from PyQt5.QtWidgets import (QMainWindow, QApplication)


os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/python3/dist-packages/PyQt5'
os.environ['DISPLAY'] = ':0'

class CustomMainWindow(QMainWindow):
    def __init__(self):
        """
        Constructor for the custom main window.
        Self.ui is essentially the main window.
        All the elements of the main window are accessible through self.ui.
        Examples: self.ui.whiteBalanceSlider, self.ui.pushButton, etc.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.arduino = ArduinoController()
     
        self.initialize_camera_controls()
        self.initialize_sliders()             
        self.initialize_stage_controls()
        self.initialize_led_buttons()


        
    def initialize_camera_controls(self):
        self.camera_controls = CameraControls()
        self.main_widget = PreviewWindow(self, self.camera_controls)


    def initialize_stage_controls(self):
        self.ui.upArrow.clicked.connect(lambda: self.arduino.move_stage(MOVE_STAGE_UP))
        self.ui.leftArrow.clicked.connect(lambda: self.arduino.move_stage(MOVE_STAGE_LEFT))
        self.ui.downArrow.clicked.connect(lambda: self.arduino.move_stage(MOVE_STAGE_DOWN))
        self.ui.rightArrow.clicked.connect(lambda: self.arduino.move_stage(MOVE_STAGE_RIGHT))
        self.ui.stage_stop_button.clicked.connect(lambda: self.arduino.move_stage(STAGE_STOP))


    def initialize_led_buttons(self):
        for i in range(1, 25):  # Assuming button names are from led_button_1 to led_button_25
            button_name = f'led_button_{i}'
            button = getattr(self.ui, button_name)  # Get the button by name from the UI
            auto_hover_button = HoverButton.replace_with_auto_hover(button)
            setattr(self, button_name, auto_hover_button)  # Replace the attribute in self with the new button
    
            # Connect hoverEnter and hoverLeave signals
            auto_hover_button.hoverEnter.connect(lambda i=i: self.arduino.send_serial_message(f'{i}'))
            auto_hover_button.hoverLeave.connect(lambda i=i: self.arduino.send_serial_message(f'{i}'))
            
        self.ui.rti_reset_button.clicked.connect(lambda: self.arduino.send_serial_message(RTI_RESET))
        self.ui.rti_reset_button.clicked.connect(self.reset_led_buttons)


    def initialize_sliders(self):
        self.white_slider = CustomSlider(self.ui.whiteBalanceSlider, "ColourGains", self.ui.whiteBalanceValueLabel, self.camera_controls)
        self.analog_gain_slider = CustomSlider(self.ui.analogGainSlider, "AnalogueGain", self.ui.analogGainValueLabel, self.camera_controls)
        self.contrast_slider = CustomSlider(self.ui.contrastSlider, "Contrast", self.ui.contrastValueLabel, self.camera_controls)
        self.sharpness_slider = CustomSlider(self.ui.sharpnessSlider, "Sharpness", self.ui.sharpnessValueLabel, self.camera_controls)
        self.saturation_slider = CustomSlider(self.ui.saturationSlider, "Saturation", self.ui.saturationValueLabel, self.camera_controls)
        self.brightness_slider = CustomSlider(self.ui.brightnessSlider, "Brightness", self.ui.brightnessValueLabel, self.camera_controls)


        self.white_slider.connect_slider_camera()
        self.analog_gain_slider.set_slider_properties(-2000, 5000, 1500)
        self.white_slider.set_slider_properties(0, 320, 160)
        self.analog_gain_slider.connect_slider_camera_1arg()
        self.contrast_slider.set_slider_properties(0, 200, 100)
        self.contrast_slider.connect_slider_camera_1arg()
        self.sharpness_slider.set_slider_properties(0, 400, 100)
        self.sharpness_slider.connect_slider_camera_1arg()
        self.saturation_slider.set_slider_properties(0, 200, 100)
        self.saturation_slider.connect_slider_camera_1arg()
        self.brightness_slider.set_slider_properties(-50, 50, 0)
        self.brightness_slider.connect_slider_camera_1arg()

    def reset_led_buttons(self):
    # Reset hover buttons
        for i in range(1, 25):  
            button_name = f'led_button_{i}'
            button = getattr(self, button_name)
            button.reset()  




        


    
    
    
