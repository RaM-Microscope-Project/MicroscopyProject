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
        self.whiteSlider = CustomSlider(self.ui.whiteBalanceSlider, "ColourGains", self.ui.whiteBalanceValueLabel, self.camera_controls)
        self.set_sliders()
        # self.analogSlider = CustomSlider(self.ui.analogGainSlider, -2000, 5000, self.ui.analogGainValueLabel, 3)
        # self.contrastSlider = CustomSlider(self.ui.contrastSlider, 0, 200, self.ui.contrastValueLabel, 2)
        # self.sharpnessSlider = CustomSlider(self.ui.sharpnessSlider, 0, 400, self.ui.sharpnessValueLabel, 4)
        # self.saturationSlider = CustomSlider(self.ui.saturationSlider, 0, 200, self.ui.saturationValueLabel, 2)
        # self.brightnessSlider = CustomSlider(self.ui.brightnessSlider, -50, 50, self.ui.brightnessValueLabel, 2)


        # ------- define the buttons -------
        
        #self.upArrowButton = CustomButtonController(self.ui.upArrow, "1")
        #self.leftArrowButton = CustomButtonController(self.ui.leftArrow, "2")
        #self.downArrowButton = CustomButtonController(self.ui.downArrow, "3")
        #self.rightArrowButton = CustomButtonController(self.ui.rightArrow, "D")
        

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


    def set_sliders(self):
         self.whiteSlider.set_slider_properties(0, 320, 160)


        


    
    
    
