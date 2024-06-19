import serial, time

class ArduinoController:
    """Controller class handling user input and updating the model."""

    def __init__(self):
        try:
            self.serial_connection = serial.Serial('/dev/ttyACM0', 9600)
            time.sleep(2)  # Give some time for the Arduino to initialize
        except Exception as e:
            print("Error: ", e)

    def handle_led(self):
        """Handle LED button click and send corresponding LED number to Arduino."""
        for led_number in range(1, 4): 
            message = f"{led_number}"
            self.send_serial_message(message)
        else:
            print("Invalid LED number. Please enter a value between 1 and 3.")

    def move_stage(self, command):
        # command = buttonController.command
        self.send_serial_message(command)

    def send_serial_message(self, message):
        """Send a serial message to the Arduino."""
        try:
            self.serial_connection.write(message.encode())
            print(f"Sent: {message.encode()}")
        except Exception as e:
            print("Error: ", e)

