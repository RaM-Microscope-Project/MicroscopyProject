from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt
import time
from PyQt5.QtGui import QFont
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from libcamera import controls
from os import mkdir

class PreviewWindow(QWidget):

    #--- MyPreviewWidget ---
    #inner class for Preview Window
    class MyPreviewWidget(QWidget):

        def __init__(self, subLayout):
            super(QWidget, self).__init__()
            self.setLayout(subLayout)

    def __init__(self, parent, camera_controls, arduino):
        super(QWidget, self).__init__(parent)
        self.camera_controls = camera_controls
        self.arduino = arduino
        self.capturing_RTI = False
        

        #--- Prepare child Preview Window ----------
        self.childPreviewLayout = QVBoxLayout()
        self.qpicamera2 = QGlPicamera2(camera_controls.picam2,
                          width=camera_controls.preview_width, height=camera_controls.preview_height,
                          keep_ar=True)
        self.childPreviewLayout.addWidget(self.qpicamera2)
        self.qpicamera2.done_signal.connect(self.capture_done)
        
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

    
    def on_Capture_Clicked(self):
        print("capturing image")
        self.btnChildCapture.setEnabled(False)
        cfg = self.camera_controls.picam2.create_still_configuration()
        timeStamp = time.strftime("%Y%m%d-%H%M%S")
        targetPath="/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/img_"+timeStamp+".jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    
    def capture_done(self, job):
        result = self.camera_controls.picam2.wait(job)
        self.btnChildCapture.setEnabled(True)
        print("- capture_done.")
        print(result)
        if self.capturing_RTI:
            self.arduino.send_serial_message(f'l{self.image_number}')
            time.sleep(0.1)
            self.image_number += 1
            if self.image_number < 24:
                print(f"taking RTI image number {self.image_number}")
                self.capture_RTI()
            else:
                self.capturing_RTI = False
                print("done capturing RTI set")

    def init_RTI(self):
        self.timeStamp = time.strftime("%d.%m.%Y-%H:%M:%S")
        mkdir(f"/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/RTI_SCAN_{self.timeStamp}")
        self.capturing_RTI = True
        self.image_number = 0
        self.capture_RTI()


    def capture_RTI(self):
        self.arduino.send_serial_message(f'L{self.image_number}')
        time.sleep(0.1)
        cfg = self.camera_controls.picam2.create_still_configuration()
        targetPath=f"/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/RTI_SCAN_{self.timeStamp}/img_{self.image_number}.jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)
