from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
# Todo: Check QButtonGroup

# ----- Camera imports -------------------------------------------

import time
from PyQt5.QtGui import QFont
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from libcamera import controls
# import os
# timeStamp = time.strftime("%Y%m%d-%H%M%S")
# targetPath = "/home/xxpepxx/Desktop/GitProject/MicroscopyProject/captures/rti_img_" + timeStamp + ".jpg"

# Ensure the directory exists
# os.makedirs(os.path.dirname(targetPath), exist_ok=True)
# picam2 = Picamera2() 
# preview_width = 1000

# # ----- I think this overwrites the previw in the class -----------------------
# preview_height = int(picam2.sensor_resolution[1] * preview_width/picam2.sensor_resolution[0])
# preview_config_raw = picam2.create_preview_configuration(main={"size": (preview_width, preview_height)},
#                                                          raw={"size": picam2.sensor_resolution})
                                                         
# picam2.configure(preview_config_raw) 

# # ---------------------------------

# picam2.set_controls({"ColourGains": (1.85, 1.85)}) #Tuple of two floating point numbers between 0.0 and 32.0.
# picam2.set_controls({"AeEnable": True})
# # picam2.set_controls({"AwbEnable": True})
# picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Long})


class PreviewWindow(QWidget):
    
    #--- MyPreviewWidget ---
    #inner class for Preview Window
    class MyPreviewWidget(QWidget):
        
        def __init__(self, subLayout):
            super(QWidget, self).__init__()
            self.setLayout(subLayout)
            
    #--- End of MyPreviewWidget ---
        

    def on_Capture_Clicked(self):
        # There are two buttons on Main/Child Window connected here,
        # identify the sender for info only, no actual use.
        sender = self.sender()
        # if sender is self.btnCapture:
        #     print("Capture button on Main Window clicked")
        if sender is self.btnChildCapture:
            print("Capture button on Child Preview Window clicked")

        self.btnChildCapture.setEnabled(False)
        
        cfg = self.camera_controls.picam2.create_still_configuration()
        
        timeStamp = time.strftime("%Y%m%d-%H%M%S")
        targetPath="/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/rti_img_"+timeStamp+".jpg"
        print("- Capture image:", targetPath)
        
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    def capture_done(self, job):
        result = self.camera_controls.picam2.wait(job)
        self.btnChildCapture.setEnabled(True)
        print("- capture_done.")
        print(result)
    
    def __init__(self, parent, camera_controls):
        super(QWidget, self).__init__(parent)
        self.camera_controls = camera_controls
        #--- Prepare child Preview Window ----------
        self.childPreviewLayout = QVBoxLayout()
        self.qpicamera2 = QGlPicamera2(camera_controls.picam2,
                          width=camera_controls.preview_width, height=camera_controls.preview_height,
                          keep_ar=True)
        self.qpicamera2.done_signal.connect(self.capture_done)
        
        self.childPreviewLayout.addWidget(self.qpicamera2)
        
        # # Capture button on Child Window

        self.btnChildCapture = QPushButton("Capture Image")
        self.btnChildCapture.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.btnChildCapture.clicked.connect(self.on_Capture_Clicked)
        self.childPreviewLayout.addWidget(self.btnChildCapture)

        # pass layout to child Preview Window
        self.myPreviewWindow = self.MyPreviewWidget(self.childPreviewLayout)

        # roughly set Preview windows size according to preview_width x preview_height
        self.myPreviewWindow.setGeometry(10, 10, camera_controls.preview_width+10, camera_controls.preview_height+100)
        self.myPreviewWindow.setWindowTitle("Camera Preview")
        self.myPreviewWindow.show()
        camera_controls.picam2.start()