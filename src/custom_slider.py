class CustomSlider:
    """
    Class to add functionality to a slider.
    Enables the camera controls to be updated when the slider is moved.
    Takes a slider, a setting, a label and a camera_controls object as arguments.
    Connects the slider to the camera_controls object and updates the label.
    """
    def __init__(self, slider, setting, label, camera_controls):
        self.slider = slider
        self.camera_controls = camera_controls
        self.label = label
        self.setting = setting
        self.update_label()
        self.slider.valueChanged.connect(self.update_label)

    def update_label(self):
        """
        Update the label with the current value of the slider.
        The value is divided by 100 to get a value between in order of units.
        """
        self.label.setText(str(self.slider.value() / 100))

    def update_camera_control_2(self, camera, setting):
        """
        Update the camera control with the value of the slider.
        Corresponds to the two parameter settings (white balance setting).
        The value is divided by 100 to get a working value for the setting.
        The second value is corrected with the value of 40 to get a working value for the white balance setting.
                                                     Based on observations, it works better with the correction.

        :param camera: The camera controls object.
        :param setting: The setting to change.
        """
        camera.set_control(setting, self.slider.value() / 100, (self.slider.value() + 40) / 100)

    def update_camera_control(self, camera, setting):
        """
        Update the camera control with the value of the slider.
        Corresponds to the single parameter settings.

        :param camera: The camera controls object.
        :param setting: The setting to change.
        """
        camera.set_control(setting, self.slider.value() / 100)

    def print_slider_value(self):
        """
        Print the value of the slider - for debugging purposes.
        """
        print(self.slider.value() / 100)

    def connect_slider_camera(self):
        """
        Connect the slider to the camera controls object.

        """
        self.slider.valueChanged.connect(lambda: self.update_camera_control_2(self.camera_controls, self.setting))

    def connect_slider_camera_1arg(self):
        """
        Connect the slider to the camera controls object.
        Only for the one parameter settings.

        Lambda explanation:
        PyQt's signals and slots mechanism connects signals (like valueChanged) to slots (methods).
        The valueChanged signal does not provide the camera_controls and setting arguments needed by update_camera_control_2.
        Using a lambda function allows us to create an inline function that captures these arguments from the current scope.
        This way, when the signal is emitted, the lambda calls update_camera_control_2 with the necessary arguments.
        """
        self.slider.valueChanged.connect(lambda: self.update_camera_control(self.camera_controls, self.setting))

    def set_slider_properties(self, minimum_value, maximum_value, initial_position):
        """
        Set the properties of the slider.

        :param minimum_value: The minimum value of the slider.
        :param maximum_value: The maximum value of the slider.
        :param initial_position: The initial position of the slider.
        """
        self.slider.setMinimum(minimum_value)
        self.slider.setMaximum(maximum_value)
        self.slider.setValue(initial_position)
