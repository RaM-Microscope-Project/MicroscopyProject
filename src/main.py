from PyQt5 import QtWidgets
from custom_main_window import CustomMainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)  #Qt Application object needed for it to run
    window = CustomMainWindow()  #instance of CutomMainWindow class
    window.show()   #display the mainwindow on the screen
    sys.exit(app.exec_())  # Start the application's event loop and exit cleanly when it's closed

