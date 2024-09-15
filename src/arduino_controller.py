import serial, time


class ArduinoController:
    """
    Controller class handling user input and updating the model.
    """

    def __init__(self):
        try:
            # the location of the serial port may change depending on the computer
            self.serial_connection = serial.Serial('/dev/ttyACM0', 9600)
            time.sleep(2)  # Give some time for the Arduino to initialize
        except Exception as e:
            print("Error: ", e)

    def move_stage(self, command):
        """
        Sends a command to the Arduino to move the stage.

        :param command: w, a, s, d to send to the Arduino.
        """
        self.send_serial_message(command)

    def send_serial_message(self, message):
        print(message)  # ToDo: remove this line
        """
        Send a serial message to the Arduino.
        
        :param message: The message to send to the Arduino.
        """
        separated_message = message + "\n"
        try:
            self.serial_connection.write(separated_message.encode())
        except Exception as e:
            print("Error: ", e)
