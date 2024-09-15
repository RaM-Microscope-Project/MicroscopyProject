from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QFont
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from libcamera import controls
import time


class CameraControls:
    """
    Controller class handling input from the GUI and sending commands to the camera.
    Sets up the initial camera settings.
    Allows to change the camera settings with the Sliders in the GUI.
    """

    def __init__(self):
        self.picam2 = Picamera2()
        self.preview_width = 1000
        self.preview_height = int(
            self.picam2.sensor_resolution[1] * self.preview_width / self.picam2.sensor_resolution[0])
        self.preview_config_raw = self.picam2.create_preview_configuration(
            main={"size": (self.preview_width, self.preview_height)},
            raw={"size": self.picam2.sensor_resolution})
        self.picam2.configure(self.preview_config_raw)
        self.picam2.set_controls({"AeEnable": True})
        self.picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Long})

        # ----- nominal value for the settings at the start of the program -----

        self.picam2.set_controls({"ColourGains": (1.6, 2)})  # between 0 and 32 red and blue
        self.picam2.set_controls({
                                     "AnalogueGain": 10})  # Floating point number - between -20? and 50+ (50+ when dark). 8 seems to be the default value.
        self.picam2.set_controls({"Contrast": (1)})  # between 0 and 32
        self.picam2.set_controls({"Sharpness": (1)})  # between 0 and 16
        self.picam2.set_controls({"Saturation": (1)})  # between 0 and 32
        self.picam2.set_controls({"Brightness": (0)})  # between -1 and 1

    def set_control(self, setting, value1, value2=None):
        """
        Set a camera setting to a specific value.

        :param setting: The setting to change.
        :param value1: The first value to set.
        :param value2: The second value to set, if the setting requires two parameters.
        """
        if value2 is not None:
            self.picam2.set_controls({setting: (value1, value2)})
        else:
            self.picam2.set_controls({setting: value1})

    def capture_image(self):
        """
        No usage so far, can be removed.
        """
        self.picam2.capture_image("captures/rtiImage.jpg")
