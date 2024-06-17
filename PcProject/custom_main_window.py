from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

from PcProject.graphical_user_interface import Ui_MainWindow


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


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