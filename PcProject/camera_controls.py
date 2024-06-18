from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QFont
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from libcamera import controls
import time

class CameraControls:
    def __init__(self):
        self.picam2 = Picamera2()
        self.preview_width = 1000
        self.preview_height = int(self.picam2.sensor_resolution[1] * self.preview_width / self.picam2.sensor_resolution[0])
        self.preview_config_raw = self.picam2.create_preview_configuration(main={"size": (self.preview_width, self.preview_height)},
                                                                           raw={"size": self.picam2.sensor_resolution})
        self.picam2.configure(self.preview_config_raw)
        self.picam2.set_controls({"AeEnable": True})
        self.picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Long})

        # ----- nominal value for the settings at the start of the program -----

        self.picam2.set_controls({"ColourGains": (1.6, 2)}) #between 0 and 32 red and blue
        self.picam2.set_controls({"AnalogueGain": 10}) #Floating point number - between -20? and 50+ (50+ when dark). 8 seems to be the default value.
        self.picam2.set_controls({"Contrast": (1)})  #between 0 and 32
        self.picam2.set_controls({"Sharpness": (1)})  #between 0 and 16
        self.picam2.set_controls({"Saturation": (1)})  #between 0 and 32 
        self.picam2.set_controls({"Brightness": (0)})  #between -1 and 1


    def set_control(self, setting, value1, value2=None):
        if value2 is not None:
            self.picam2.set_controls({setting: (value1, value2)})
        else:
            self.picam2.set_controls({setting: value1})

    # def start(self):
    #     self.picam2.start()

    # def create_still_configuration(self):
    #     return self.picam2.create_still_configuration()

    # def switch_mode_and_capture_file(self, cfg, target_path, signal_function=None):
    #     self.picam2.switch_mode_and_capture_file(cfg, target_path, signal_function)

    # def wait(self, job):
    #     return self.picam2.wait(job)
