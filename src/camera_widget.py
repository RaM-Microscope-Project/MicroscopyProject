from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QFont
from picamera2.previews.qt import QGlPicamera2
from os import mkdir
import time
import cv2
import numpy
import os
import subprocess
from pathlib import Path

class Camera_widget(QWidget):

    #--- MyPreviewWidget ---
    #inner class for Preview Window
    class MyPreviewWidget(QWidget):

        def __init__(self, subLayout):
            super(QWidget, self).__init__()
            self.setLayout(subLayout)
            self.target_path=self.get_target_path()
            print(self.target_path)


    def get_target_path(self):
        """Return the absolute path to the user's Desktop directory,
        independent of username or system language."""
        try:
            # Try to get the localized Desktop path using xdg-user-dir
            desktop_path = subprocess.run(
                ["xdg-user-dir", "DESKTOP"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # If the result is empty, fall back
            if not desktop_path:
                raise ValueError("xdg-user-dir returned empty path")

        except Exception:
            # Fallback to the standard Desktop folder in the user's home
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        return Path(desktop_path)

    def __init__(self, parent, camera_controls, arduino):
        super(QWidget, self).__init__(parent)
        self.uiWindow = parent
        self.camera_controls = camera_controls
        self.arduino = arduino

        #some variables to store the active state of the automation features
        self.capturing_RTI = False
        self.capturing_SP = False
        self.capturing_FS = False
        self.auto_focus = False
        self.count = 0
        self.prev_blur_value = 8
        

        #--- Prepare child Preview Window ----------
        self.childPreviewLayout = QVBoxLayout()
        self.qpicamera2 = QGlPicamera2(camera_controls.picam2,
                          width=camera_controls.preview_width,
                          height=camera_controls.preview_height,
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

    #capture an image
    def on_Capture_Clicked(self):
        print("capturing image")
        self.btnChildCapture.setEnabled(False)
        cfg = self.camera_controls.picam2.create_still_configuration()
        timeStamp = time.strftime("%Y%m%d-%H%M%S")
        targetPath="/home/microscopi/Desktop/img_"+timeStamp+".jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    #this function is called whenever an image capture is finished
    def capture_done(self, job):
        result = self.camera_controls.picam2.wait(job)
        self.btnChildCapture.setEnabled(True)
        #call the capture_set function to capture the next image in the image set right away
        self.capture_set(result)
    
    #this function checks what set is being captured, send the arduino controller class commands accordingly and captures the next image in the set
    def capture_set(self, result):
        if self.capturing_RTI:
            self.arduino.serial(f'LED0{self.count}')
            time.sleep(0.1)
            self.count += 1
            if self.count < 24:
                print(f"taking RTI image number {self.count}")
                self.capture_RTI()
            else:
                self.capturing_RTI = False
                self.uiWindow.ui.progressBar.setValue(0)
                self.uiWindow.ui.progressBar.hide()
                print("done capturing RTI set")
        
        if self.capturing_SP:
            self.stereo_photography(2)
            self.capturing_SP = False

        if self.auto_focus:
            self.autofocus(result, 15)
            if self.auto_focus:
                self.test_focus()
        
        if self.capturing_FS:
            self.focus_stack()


    #initialises the RTI function by making a directory and setting the variables
    def init_RTI(self):
        self.arduino.serial(f'LED_B{self.uiWindow.ui.inputBox_RTI.value()}')
        self.timeStamp = time.strftime("%d.%m.%Y-%H:%M:%S")
        mkdir(f"/home/microscopi/Desktop/RTI_SCAN_{self.timeStamp}")
        self.capturing_RTI = True
        self.count = 0
        self.capture_RTI()

    #excecutes the RTI captures by setting the LEDs and capturing an image
    def capture_RTI(self):
        self.uiWindow.ui.progressBar.show()
        self.uiWindow.ui.progressBar.setValue(int((self.count / 24) * 100))
        time.sleep(0.1)
        self.arduino.serial(f'LED1{self.count}')
        time.sleep(0.1)
        #capture an image
        cfg = self.camera_controls.picam2.create_still_configuration()
        targetPath=f"/home/microscopi/Desktop/RTI_SCAN_{self.timeStamp}/img_{self.count}.jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    #performs a stereo photography capture by taking two pictures and moving the stage in between
    def stereo_photography(self, number):
        if (number == 1):#make the directory first time this function is called
            self.timeStamp = time.strftime("%d.%m.%Y-%H:%M:%S")
            mkdir(f"/home/microscopi/Desktop/SP_SCAN_{self.timeStamp}")

        delta = self.uiWindow.ui.inputBox_SP.value()
        self.arduino.serial(f'SP{number}{delta}')
        self.capturing_SP = True

        time.sleep(0.5*delta)

        #capture an image
        cfg = self.camera_controls.picam2.create_still_configuration()
        targetPath=f"/home/microscopi/Desktop/SP_SCAN_{self.timeStamp}/img_{number}_{delta}mm.jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

    #performs a focus stacking scan
    def focus_stack(self):
        height = self.uiWindow.ui.inputBox_FS_h.value()
        n = self.uiWindow.ui.inputBox_FS_n.value()
        delta = height/n
        self.capturing_FS = True
        self.uiWindow.ui.progressBar.show()
        self.uiWindow.ui.progressBar.setValue(int((self.count / n) * 100))

        if self.count == 0:#make the directory first time this function is called
            #self.arduino.serial(f'Z0')
            self.timeStamp = time.strftime("%d.%m.%Y-%H:%M:%S")
            mkdir(f"/home/microscopi/Desktop/FS_SCAN_{self.timeStamp}")
            time.sleep(5)

        #capture an image
        cfg = self.camera_controls.picam2.create_still_configuration()
        targetPath=f"/home/microscopi/Desktop/FS_SCAN_{self.timeStamp}/img_{self.count + 1}_{delta}mm.jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath, signal_function=self.qpicamera2.signal_done)

        time.sleep(0.1)
        self.arduino.serial(f'FS{delta}')
        
        self.count += 1
        if self.count == n:
            self.count = 0
            self.capturing_FS = False
            self.uiWindow.ui.progressBar.hide()
            self.uiWindow.ui.progressBar.setValue(0)

    #used for debugging purposes
    def test_focus(self):
        print("test autofocus")
        self.auto_focus = True
        cfg = self.camera_controls.picam2.create_preview_configuration()
        img = self.camera_controls.picam2.switch_mode_and_capture_array(cfg, signal_function=self.qpicamera2.signal_done)
        
    #performs the autofocus function
    def autofocus(self, img, n):
        self.uiWindow.ui.progressBar.show()
        self.uiWindow.ui.progressBar.setValue(int((self.count / n) * 100))
        
        self.count += 1
        crop = 50

        #exclude the edges of the image, as you want the center to be in focus
        img_center = img[(int((img.shape[0]/2)-crop)):(int((img.shape[0]/2)+crop)),
                         (int((img.shape[1]/2)-crop)):(int((img.shape[1]/2)+crop))]

        #use the laplacian oparator to get a value for the sharpness
        #value depends on the sample but in general:
        #0 - 3 is completely blurred, 3 - 8 is blurry, 9 + is in focus
        
        blur_value = round(numpy.std(cv2.Laplacian(img_center, cv2.CV_64F)), 2)
        self.arduino.serial(f"AF{blur_value}")

        if blur_value > 8:#if it is getting sharp, go into fine control mode
            self.arduino.serial("AFF")
            
        if self.count == n:#if the loop is done but the image is not in focus at all, restart
            if blur_value < 5:
                time.sleep(0.1)
                print("autofocus failed, restarting...")

            else:#else, done
                time.sleep(0.1)
                self.auto_focus = False
                self.uiWindow.ui.progressBar.hide()

            self.arduino.serial("AFS")
            self.count = 0
            self.uiWindow.ui.progressBar.setValue(0)


        

    
