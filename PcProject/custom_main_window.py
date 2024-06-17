from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

from PcProject.graphical_user_interface import Ui_MainWindow
from custom_slider import CustomSlider


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