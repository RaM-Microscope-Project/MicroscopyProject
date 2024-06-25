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
        Constructor for the custom main window and inherits from the
                                    application design in QT Designer.
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
        self.whiteSlider = CustomSlider(self.ui.whiteBalanceSlider, 0, 320, self.ui.whiteBalanceValueLabel, 2)
        self.analogSlider = CustomSlider(self.ui.analogGainSlider, -2000, 5000, self.ui.analogGainValueLabel, 3)
        self.contrastSlider = CustomSlider(self.ui.contrastSlider, 0, 200, self.ui.contrastValueLabel, 2)
        self.sharpnessSlider = CustomSlider(self.ui.sharpnessSlider, 0, 400, self.ui.sharpnessValueLabel, 4)
        self.saturationSlider = CustomSlider(self.ui.saturationSlider, 0, 200, self.ui.saturationValueLabel, 2)
        self.brightnessSlider = CustomSlider(self.ui.brightnessSlider, -50, 50, self.ui.brightnessValueLabel, 2)


        # Todo:define method for this
        self.whiteSlider.slider.valueChanged.connect(lambda: 
                self.whiteSlider.update_camera_control_2(self.camera_controls, "ColourGains"))
        self.analogSlider.slider.valueChanged.connect(lambda: 
                self.analogSlider.update_camera_control(self.camera_controls, "AnalogueGain"))
        self.contrastSlider.slider.valueChanged.connect(lambda: 
                self.contrastSlider.update_camera_control(self.camera_controls, "Contrast"))
        self.sharpnessSlider.slider.valueChanged.connect(lambda: 
                self.sharpnessSlider.update_camera_control(self.camera_controls, "Sharpness"))
        self.saturationSlider.slider.valueChanged.connect(lambda: 
                self.saturationSlider.update_camera_control(self.camera_controls, "Saturation"))
        self.brightnessSlider.slider.valueChanged.connect(lambda: 
                self.brightnessSlider.update_camera_control(self.camera_controls, "Brightness"))


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


        

        #  Todo: define method or a for loop for this
        self.let_button_controllers = []
        for i in range(1, 25):
            button = getattr(self.ui, f"led_button_{i}")
            self.let_button_controllers.append(LedButtonController(button))
        #     button.clicked.connect(lambda: self.arduino.send_serial_message(str(i)))



        self.ui.led_button_1.clicked.connect(lambda: self.arduino.send_serial_message("1"))
        self.ui.led_button_2.clicked.connect(lambda: self.arduino.send_serial_message("2"))
        self.ui.led_button_3.clicked.connect(lambda: self.arduino.send_serial_message("3"))
        self.ui.led_button_4.clicked.connect(lambda: self.arduino.send_serial_message("4"))
        self.ui.led_button_5.clicked.connect(lambda: self.arduino.send_serial_message("5"))
        self.ui.led_button_6.clicked.connect(lambda: self.arduino.send_serial_message("6"))
        self.ui.led_button_7.clicked.connect(lambda: self.arduino.send_serial_message("7"))
        self.ui.led_button_8.clicked.connect(lambda: self.arduino.send_serial_message("8"))
        self.ui.led_button_9.clicked.connect(lambda: self.arduino.send_serial_message("9"))
        self.ui.led_button_10.clicked.connect(lambda: self.arduino.send_serial_message("10"))
        self.ui.led_button_11.clicked.connect(lambda: self.arduino.send_serial_message("11"))
        self.ui.led_button_12.clicked.connect(lambda: self.arduino.send_serial_message("12"))
        self.ui.led_button_13.clicked.connect(lambda: self.arduino.send_serial_message("13"))
        self.ui.led_button_14.clicked.connect(lambda: self.arduino.send_serial_message("14"))
        self.ui.led_button_15.clicked.connect(lambda: self.arduino.send_serial_message("15"))
        self.ui.led_button_16.clicked.connect(lambda: self.arduino.send_serial_message("16"))
        self.ui.led_button_17.clicked.connect(lambda: self.arduino.send_serial_message("17"))
        self.ui.led_button_18.clicked.connect(lambda: self.arduino.send_serial_message("18"))
        self.ui.led_button_19.clicked.connect(lambda: self.arduino.send_serial_message("19"))
        self.ui.led_button_20.clicked.connect(lambda: self.arduino.send_serial_message("20"))
        self.ui.led_button_21.clicked.connect(lambda: self.arduino.send_serial_message("21"))
        self.ui.led_button_22.clicked.connect(lambda: self.arduino.send_serial_message("22"))
        self.ui.led_button_23.clicked.connect(lambda: self.arduino.send_serial_message("23"))
        self.ui.led_button_24.clicked.connect(lambda: self.arduino.send_serial_message("24"))


        
        

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())
    
    
    
