class CustomSlider:
    def __init__(self, slider, setting, label, camera_controls):
        self.slider = slider
        self.camera_controls = camera_controls
        self.label = label
        self.update_label()
        self.slider.valueChanged.connect(self.update_label)
        self.connect_slider_camera(setting)
        

    def update_label(self):
        self.label.setText(str(self.slider.value()/100))

    def update_camera_control_2(self, camera, setting):
        camera.set_control(setting, self.slider.value()/100, (self.slider.value()+40)/100)

    def update_camera_control(self, camera, setting):
        camera.set_control(setting, self.slider.value()/100)

    def print_slider_value(self):
        print(self.slider.value()/100)

    def connect_slider_camera(self, setting):
        self.slider.valueChanged.connect(lambda: self.update_camera_control_2(self.camera_controls, "ColourGains"))

    def set_slider_properties(self, minimum_value, maximum_value, initial_position):
        self.slider.setMinimum(minimum_value)
        self.slider.setMaximum(maximum_value)
        self.slider.setValue(initial_position)