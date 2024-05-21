import serial
import time

# Establish a serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the device name and baud rate

def send_command(command):
    ser.write(command.encode())  # Send single character command to Arduino

try:
    while True:
        input_key = input("Enter command (1-6) to light up the corresponding LED or 'q' to quit: ")
        if input_key in ['1', '2', '3', '4', '5', '6']:
            send_command(input_key)
        elif input_key == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid command. Please enter a number from 1 to 6 or 'q' to quit.")
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()  # Close the serial connection
