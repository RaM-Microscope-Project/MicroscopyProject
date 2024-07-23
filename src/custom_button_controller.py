class CustomButtonController:
    def __init__(self, arduino):
        self.arduino = arduino

    def connect_button_with_message(self, button, message):
        button.clicked.connect(lambda: self.arduino.send_serial_message(message))


        


    