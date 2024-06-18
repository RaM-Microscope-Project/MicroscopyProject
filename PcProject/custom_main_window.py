import os, sys, platform

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDial,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout
)

from PyQt5 import QtCore, QtWidgets

from graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider
from preview_window import PreviewWindow

# ----- Camera imports -------------------------------------------

import time
from importlib.metadata import version
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel, QCheckBox,
                             QWidget, QTabWidget, QVBoxLayout, QGridLayout)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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

        self.main_widget = PreviewWindow(self)

        # ------- define the sliders -------
        self.whiteSlider = CustomSlider(self.ui.whiteBalanceSlider, 0, 400, self.ui.whiteBalanceValueLabel)
        self.analogSlider = CustomSlider(self.ui.analogGainSlider, 0, 100, self.ui.analogGainValueLabel)
        self.contrastSlider = CustomSlider(self.ui.contrastSlider, 0, 100, self.ui.contrastValueLabel)
        self.sharpnessSlider = CustomSlider(self.ui.sharpnessSlider, 0, 100, self.ui.sharpnessValueLabel)
        self.saturationSlider = CustomSlider(self.ui.saturationSlider, 0, 100, self.ui.saturationValueLabel)
        self.brightnessSlider = CustomSlider(self.ui.brightnessSlider, 0, 100, self.ui.brightnessValueLabel)


import resources_rc

if __name__ == "__main__":
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())