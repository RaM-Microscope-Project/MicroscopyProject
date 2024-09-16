# **Microscopy Project**

*This repository contains the software of a Raspberry Pi-based microscope, with RTI functionalities.
The software provides a GUI for controlling the stage, camera, and LEDs of the RTI dome, and is 
responsible for correctly handling the user inputs.*

## **Description**

**Key Features**
* *Graphical User Interface*: Split into three sections, namely stage control, camera control and LED control.
Currently, the GUI aesthetics can be improved. The focus in the project was strictly on functionality.
* *Arduino Integration*: The software communicates with the Arduino board to control the stage and LEDs vial serial
communication. The communication is simple: The RPI sends the commands *W, A, S, D* for the stage control,
and integers from 1 to 25 for the LED control.

**Technologies Used:**
* *Python*: Main programming language.
* *PyQt*: Used for the GUI framework.
* *PyQt Designer*: A tool used to design the GUI visually, which was then converted into Python for further integration.
The GUI was designed on a Windows machine, and then transferred to the Raspberry Pi. However, the machine used should
for the Designer should not matter.
* *Arduino*: Used for the stage and LED control.

## **.UI to .py Conversion**
Again, the GUI was designed using PyQt Designer. The output of this program is a .ui file, which 
is then converted into a .py file using the following command:
```bash
- pyuic5 -x <filename>.ui -o <filename>.py
```

## **Usage**
To run the code, execute this bash command in the src directory:
```bash
python main.py
```
Alternatively, you can run the code from the main.py file.





