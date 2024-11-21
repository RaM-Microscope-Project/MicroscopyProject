from PyQt5 import QtWidgets
from custom_main_window import CustomMainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())

