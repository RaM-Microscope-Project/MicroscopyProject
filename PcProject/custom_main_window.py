import os, sys, platform
from PyQt5 import QtCore, QtWidgets


# ----- Imports of the other classes -------------------------------------------
from graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider
from preview_window import PreviewWindow
from camera_controls import CameraControls
from arduino_controller import ArduinoController

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

        self.arduino = ArduinoController()
        self.arduino.handle_led_button_click()

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())
