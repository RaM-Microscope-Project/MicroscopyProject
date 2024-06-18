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


# ----- Camera imports -------------------------------------------

import time
from importlib.metadata import version
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel, QCheckBox,
                             QWidget, QTabWidget, QVBoxLayout, QGridLayout)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

WINDOW_SIZE = 350
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"

global_color_gain = 1.85

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from picamera2 import __name__ as picamera2_name
from libcamera import controls
picam2 = Picamera2() 


preview_width= 1000
preview_height = int(picam2.sensor_resolution[1] * preview_width/picam2.sensor_resolution[0])
preview_config_raw = picam2.create_preview_configuration(main={"size": (preview_width, preview_height)},
                                                         raw={"size": picam2.sensor_resolution})
                                                         
picam2.configure(preview_config_raw)
picam2.set_controls({"ColourGains": (global_color_gain, global_color_gain)}) #Tuple of two floating point numbers between 0.0 and 32.0.
picam2.set_controls({"AeEnable": True})
# picam2.set_controls({"AwbEnable": True})
picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Long})


class PreviewWindow(QWidget):
    
    #--- MyPreviewWidget ---
    #inner class for Preview Window
    class MyPreviewWidget(QWidget):
        
        def __init__(self, subLayout):
            super(QWidget, self).__init__()
            self.setLayout(subLayout)
            
    #--- End of MyPreviewWidget ---
        

    # def on_Capture_Clicked(self):
    #     # There are two buttons on Main/Child Window connected here,
    #     # identify the sender for info only, no actual use.
    #     sender = self.sender()
    #     if sender is self.btnCapture:
    #         print("Capture button on Main Window clicked")
    #     if sender is self.btnChildCapture:
    #         print("Capture button on Child Preview Window clicked")

    #     self.btnCapture.setEnabled(False)
        
    #     cfg = picam2.create_still_configuration()
        
    #     timeStamp = time.strftime("%Y%m%d-%H%M%S")
    #     targetPath="/home/pi/Desktop/img_"+timeStamp+".jpg"
    #     print("- Capture image:", targetPath)
        
    #     picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    # def capture_done(self, job):
    #     result = picam2.wait(job)
    #     self.btnCapture.setEnabled(True)
    #     print("- capture_done.")
    #     print(result)
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        
        #--- Prepare child Preview Window ----------
        self.childPreviewLayout = QVBoxLayout()
        self.qpicamera2 = QGlPicamera2(picam2,
                          width=preview_width, height=preview_height,
                          keep_ar=True)
        # self.qpicamera2.done_signal.connect(self.capture_done)
        
        self.childPreviewLayout.addWidget(self.qpicamera2)
        
        # # Capture button on Child Window

        # self.btnChildCapture = QPushButton("Capture Image")
        # self.btnChildCapture.setFont(QFont("Helvetica", 13, QFont.Bold))
        # self.btnChildCapture.clicked.connect(self.on_Capture_Clicked)

        # self.childPreviewLayout.addWidget(self.btnChildCapture)

        # pass layout to child Preview Window
        self.myPreviewWindow = self.MyPreviewWidget(self.childPreviewLayout)

        # roughly set Preview windows size according to preview_width x preview_height
        self.myPreviewWindow.setGeometry(10, 10, preview_width+10, preview_height+100)
        self.myPreviewWindow.setWindowTitle("Camera Preview")
        self.myPreviewWindow.show()
        picam2.start()