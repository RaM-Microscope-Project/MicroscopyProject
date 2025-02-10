import serial, time

class ArduinoController:
    """Controller class handling user input and updating the model."""

    def __init__(self):
        try:
            self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)#try connecting to USB
            time.sleep(2)  # Give some time for the Arduino to initialize
        except Exception as e:
            print("Error: ", e)
            self.serial_connection = serial.Serial('/dev/ttyAMA0', 115200)#connect through UART

    def set_speed(self, value):
        self.serial(f"SPEED{value}")

    def serial(self, message):
        print (message)
        """Send a serial message to the Arduino."""
        separated_message = message + "\n"
        try:
            self.serial_connection.write(separated_message.encode())
        except Exception as e:
            print("Error: ", e)
    

    

