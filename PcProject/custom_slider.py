class CustomSlider:
    def __init__(self, slider, minimum, maximum, label, position_divisor):
        self.slider = slider
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.label = label
        self.slider.valueChanged.connect(self.update_label)
        self.set_slider_position(position_divisor)


    def set_slider_position(self, position_divisor):
        middle_value = (self.slider.minimum() + self.slider.maximum()) // position_divisor
        self.slider.setValue(middle_value)

    def update_label(self):
        self.label.setText(str(self.slider.value()/100))

    def update_camera_control_2(self, camera, setting):
        camera.set_control(setting, self.slider.value()/100, (self.slider.value()+40)/100)

    def update_camera_control(self, camera, setting):
        camera.set_control(setting, self.slider.value()/100)

    def print_slider_value(self):
        print(self.slider.value()/100)
