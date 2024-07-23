import os, sys, platform
from PyQt5 import QtCore, QtWidgets


# ----- Imports of the other classes -------------------------------------------
from graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider
from preview_window import PreviewWindow
from camera_controls import CameraControls
from arduino_controller import ArduinoController
from custom_button_controller import CustomButtonController
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

     
        self.camera_controls = CameraControls()
        self.main_widget = PreviewWindow(self, self.camera_controls)



        # ------- define the sliders -------
        self.white_slider = CustomSlider(self.ui.whiteBalanceSlider, "ColourGains", self.ui.whiteBalanceValueLabel, self.camera_controls)
        self.analog_gain_slider = CustomSlider(self.ui.analogGainSlider, "AnalogueGain", self.ui.analogGainValueLabel, self.camera_controls)
        self.contrast_slider = CustomSlider(self.ui.contrastSlider, "Contrast", self.ui.contrastValueLabel, self.camera_controls)
        self.sharpness_slider = CustomSlider(self.ui.sharpnessSlider, "Sharpness", self.ui.sharpnessValueLabel, self.camera_controls)
        self.saturation_slider = CustomSlider(self.ui.saturationSlider, "Saturation", self.ui.saturationValueLabel, self.camera_controls)
        self.brightness_slider = CustomSlider(self.ui.brightnessSlider, "Brightness", self.ui.brightnessValueLabel, self.camera_controls)

        self.initialize_sliders()             

        # ------- test the arduino controller -------

        self.arduino = ArduinoController()
        # self.arduino.handle_led()

        self.ui.upArrow.clicked.connect(lambda: self.arduino.move_stage("s"))
        self.ui.leftArrow.clicked.connect(lambda: self.arduino.move_stage("d"))
        self.ui.downArrow.clicked.connect(lambda: self.arduino.move_stage("w"))
        self.ui.rightArrow.clicked.connect(lambda: self.arduino.move_stage("a"))
        self.ui.stage_stop_button.clicked.connect(lambda: self.arduino.move_stage("q"))


        led_button_controller = CustomButtonController(self.arduino)

        for i in range(1, 25):
                button = getattr(self.ui, f'led_button_{i}') # dynamically get the button by name
                led_button_controller.connect_button_with_message(button, str(i))


        self.ui.rti_reset_button.clicked.connect(lambda: self.arduino.send_serial_message("m"))


    def initialize_sliders(self):
         self.white_slider.set_slider_properties(0, 320, 160)
         self.white_slider.connect_slider_camera()
         self.analog_gain_slider.set_slider_properties(-2000, 5000, 1500)
         self.analog_gain_slider.connect_slider_camera_1arg()
         self.contrast_slider.set_slider_properties(0, 200, 100)
         self.contrast_slider.connect_slider_camera_1arg()
         self.sharpness_slider.set_slider_properties(0, 400, 100)
         self.sharpness_slider.connect_slider_camera_1arg()
         self.saturation_slider.set_slider_properties(0, 200, 100)
         self.saturation_slider.connect_slider_camera_1arg()
         self.brightness_slider.set_slider_properties(-50, 50, 0)
         self.brightness_slider.connect_slider_camera_1arg()


        


    
    
    
