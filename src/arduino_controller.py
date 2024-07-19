import serial, time

class ArduinoController:
    """Controller class handling user input and updating the model."""

    def __init__(self):
        try:
            self.serial_connection = serial.Serial('/dev/ttyACM0', 9600)
            time.sleep(2)  # Give some time for the Arduino to initialize
        except Exception as e:
            print("Error: ", e)


    def move_stage(self, command):
        # command = buttonController.command
        self.send_serial_message(command)

    def send_serial_message(self, message):
        print (message)
        """Send a serial message to the Arduino."""
        separated_message = message + "\n"
        try:
            self.serial_connection.write(separated_message.encode())
            # print(f"Sent: {separated_message.encode()}")
        except Exception as e:
            print("Error: ", e)
    

    

