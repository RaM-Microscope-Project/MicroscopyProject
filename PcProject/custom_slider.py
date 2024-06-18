class CustomSlider:
    def __init__(self, slider, minimum, maximum, label):
        self.slider = slider
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.label = label
        self.slider.valueChanged.connect(self.update_label)
        self.set_slider_to_middle()


    def set_slider_to_middle(self):
        middle_value = (self.slider.minimum() + self.slider.maximum()) // 2
        self.slider.setValue(middle_value)

    def update_label(self):
        self.label.setText(str(self.slider.value()/100))

    def update_camera_control(self, camera, setting, value):
        camera.set_control(setting, value, value)

    def print_slider_value(self):
        print(self.slider.value()/100)