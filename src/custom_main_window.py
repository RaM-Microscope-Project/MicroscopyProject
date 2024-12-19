# Class created by MateiObrocea

import os
from UI import Ui_MainWindow
from PyQt5.QtWidgets import (QMainWindow)
from custom_slider import CustomSlider
from hover_button import HoverButton
from camera_widget import Camera_widget
from camera_controls import CameraControls
from arduino_controller import ArduinoController


os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/python3/dist-packages/PyQt5'
os.environ['DISPLAY'] = ':0'

class CustomMainWindow(QMainWindow):
    def __init__(self):
        """
        Constructor for the custom main window.
        Self.ui is essentially the main window.
        All the elements of the main window are accessible through self.ui.
        Examples: self.ui.whiteBalanceSlider, self.ui.pushButton, etc.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.arduino = ArduinoController()
        
     
        self.initialize_camera_controls()           
        self.initialize_stage_controls()
        self.initialize_led_buttons()
        self.initialize_scan_buttons()
        self.ui.progressBar.hide()
        
    def initialize_scan_buttons(self):
        self.ui.scan_rti.pressed.connect(self.camera_widget.init_RTI)
        self.ui.scan_sp.pressed.connect(lambda: self.camera_widget.stereo_photography(1))
        self.ui.scan_fs.pressed.connect(self.camera_widget.focus_stack)

        
    def initialize_camera_controls(self):
        self.camera_controls = CameraControls()
        self.camera_widget = Camera_widget(self, self.camera_controls, self.arduino)
        self.initialize_sliders()
        self.ui.focus_button_min.pressed.connect(lambda: self.arduino.move_stage("Z-"))
        self.ui.focus_button_plus.pressed.connect(lambda: self.arduino.move_stage("Z+"))
        self.ui.focus_button_min.released.connect(lambda: self.arduino.move_stage("ZS"))
        self.ui.focus_button_plus.released.connect(lambda: self.arduino.move_stage("ZS"))
        self.ui.focus_button_auto.clicked.connect(lambda: self.camera_widget.test_focus())


    def initialize_stage_controls(self):
        self.ui.speed_slider.valueChanged.connect(self.arduino.set_speed)
        self.ui.upArrow.pressed.connect(lambda: self.arduino.move_stage("Y+"))
        self.ui.upArrow.released.connect(lambda: self.arduino.move_stage("YS"))
        self.ui.leftArrow.pressed.connect(lambda: self.arduino.move_stage("X-"))
        self.ui.leftArrow.released.connect(lambda: self.arduino.move_stage("XS"))
        self.ui.downArrow.pressed.connect(lambda: self.arduino.move_stage("Y-"))
        self.ui.downArrow.released.connect(lambda: self.arduino.move_stage("YS"))
        self.ui.rightArrow.pressed.connect(lambda: self.arduino.move_stage("X+"))
        self.ui.rightArrow.released.connect(lambda: self.arduino.move_stage("XS"))
        self.ui.stage_stop_button.clicked.connect(lambda: self.arduino.move_stage("CAL"))

    def initialize_led_buttons(self):
        for i in range(1, 25):  # Assuming button names are from led_button_1 to led_button_25
            button_name = f'led_button_{i}'
            button = getattr(self.ui, button_name)  # Get the button by name from the UI
            auto_hover_button = HoverButton.replace_with_auto_hover(button)
            setattr(self, button_name, auto_hover_button)  # Replace the attribute in self with the new button
    
            # Connect hoverEnter and hoverLeave signals
            auto_hover_button.hoverEnter.connect(lambda i=i: self.arduino.serial(f'LED1{i-1}'))
            auto_hover_button.hoverLeave.connect(lambda i=i: self.arduino.serial(f'LED0{i-1}'))
            
        self.ui.rti_reset_button.clicked.connect(lambda: self.arduino.serial(RTI_RESET))
        self.ui.rti_reset_button.clicked.connect(self.reset_led_buttons)


    def initialize_sliders(self):
        self.white_slider = CustomSlider(self.ui.whiteBalanceSlider, "ColourGains", self.ui.whiteBalanceValueLabel, self.camera_controls)
        self.analog_gain_slider = CustomSlider(self.ui.analogGainSlider, "AnalogueGain", self.ui.analogGainValueLabel, self.camera_controls)
        self.contrast_slider = CustomSlider(self.ui.contrastSlider, "Contrast", self.ui.contrastValueLabel, self.camera_controls)
        self.sharpness_slider = CustomSlider(self.ui.sharpnessSlider, "Sharpness", self.ui.sharpnessValueLabel, self.camera_controls)
        self.saturation_slider = CustomSlider(self.ui.saturationSlider, "Saturation", self.ui.saturationValueLabel, self.camera_controls)
        self.brightness_slider = CustomSlider(self.ui.brightnessSlider, "Brightness", self.ui.brightnessValueLabel, self.camera_controls)


        self.white_slider.connect_slider_camera()
        self.analog_gain_slider.set_slider_properties(-2000, 5000, 1500)
        self.white_slider.set_slider_properties(0, 320, 160)
        self.analog_gain_slider.connect_slider_camera_1arg()
        self.contrast_slider.set_slider_properties(0, 200, 100)
        self.contrast_slider.connect_slider_camera_1arg()
        self.sharpness_slider.set_slider_properties(0, 400, 100)
        self.sharpness_slider.connect_slider_camera_1arg()
        self.saturation_slider.set_slider_properties(0, 200, 100)
        self.saturation_slider.connect_slider_camera_1arg()
        self.brightness_slider.set_slider_properties(-50, 50, 0)
        self.brightness_slider.connect_slider_camera_1arg()

    def reset_led_buttons(self):
    # Reset hover buttons
        for i in range(1, 25):  
            button_name = f'led_button_{i}'
            button = getattr(self, button_name)
            button.reset()  






        


    
    
    
