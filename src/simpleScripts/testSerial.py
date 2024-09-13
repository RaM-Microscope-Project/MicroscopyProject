import serial
import time

# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust '/dev/ttyUSB0' to your serial port

def send_command(command):
    ser.write(command.encode())
    time.sleep(0.1)  # Short delay to allow the Arduino to process the command

try:
    while True:
        print("Enter 1, 2, or 3 to toggle the corresponding LED (or 'q' to quit): ")
        user_input = input().strip()

        if user_input == 'q':
            break
        elif user_input in ['1', '2', '3']:
            send_command(user_input)
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
