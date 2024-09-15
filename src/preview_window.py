from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt
import time
from PyQt5.QtGui import QFont
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from libcamera import controls


class PreviewWindow(QWidget):
    """
    Class for the preview window.
    Separate preview window with a button underneath to capture an image at a designated location.
    Capturing mechanism inspired from: https://coxxect.blogspot.com/2023/12/using-raspberry-pi-camera-in.html
    """
    class MyPreviewWidget(QWidget):

        def __init__(self, subLayout):
            super(QWidget, self).__init__()
            self.setLayout(subLayout)

    def on_Capture_Clicked(self):
        """
        Capture an image when the button is clicked.
        Image is saved at a designated location - make sure the path is correct.
        The name of the image is the current timestamp.
        """
        sender = self.sender()
        if sender is self.btnChildCapture:
            print("Capture button on Child Preview Window clicked")
        self.btnChildCapture.setEnabled(False)
        cfg = self.camera_controls.picam2.create_still_configuration()
        timeStamp = time.strftime("%Y%m%d-%H%M%S")
        targetPath = "/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/rti_img_" + timeStamp + ".jpg"
        print("- Capture image:", targetPath)
        self.camera_controls.picam2.switch_mode_and_capture_file(cfg, targetPath,
                                                                 signal_function=self.qpicamera2.signal_done)

    def capture_done(self, job):
        """
        Handle the capture done signal.
        Enable the button after the capture is done.
        """
        result = self.camera_controls.picam2.wait(job)
        self.btnChildCapture.setEnabled(True)
        print("- capture_done.")
        print(result)

    def __init__(self, parent, camera_controls):
        """
        Constructor for the preview window.

        :param parent: The parent widget.
        :param camera_controls: The camera controls object
        """
        super(QWidget, self).__init__(parent)
        self.camera_controls = camera_controls
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
        self.myPreviewWindow.setGeometry(10, 10, camera_controls.preview_width + 10,
                                         camera_controls.preview_height + 100)
        self.myPreviewWindow.setWindowTitle("Camera Preview")
        self.myPreviewWindow.show()
        camera_controls.picam2.start()
