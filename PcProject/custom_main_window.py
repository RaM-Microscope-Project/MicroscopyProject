import os, sys, platform
from PyQt5 import QtCore, QtWidgets


# ----- Imports of the other classes -------------------------------------------
from graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider
from preview_window import PreviewWindow
from camera_controls import CameraControls

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
        self.whiteSlider = CustomSlider(self.ui.whiteBalanceSlider, 0, 400, self.ui.whiteBalanceValueLabel)
        self.analogSlider = CustomSlider(self.ui.analogGainSlider, 0, 100, self.ui.analogGainValueLabel)
        self.contrastSlider = CustomSlider(self.ui.contrastSlider, 0, 100, self.ui.contrastValueLabel)
        self.sharpnessSlider = CustomSlider(self.ui.sharpnessSlider, 0, 100, self.ui.sharpnessValueLabel)
        self.saturationSlider = CustomSlider(self.ui.saturationSlider, 0, 100, self.ui.saturationValueLabel)
        self.brightnessSlider = CustomSlider(self.ui.brightnessSlider, 0, 100, self.ui.brightnessValueLabel)
        
        self.whiteSlider.slider.valueChanged.connect(lambda: self.whiteSlider.update_camera_control(self.camera_controls, "ColourGains", self.whiteSlider.slider.value()/100))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())