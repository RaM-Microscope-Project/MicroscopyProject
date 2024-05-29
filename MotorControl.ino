/* 
  Example sketch to control a 28BYJ-48 stepper motor 
  with ULN2003 driver board and Arduino UNO. 
  More info: https://www.makerguides.com 
*/

#include "Stepper.h"
#include <AccelStepper.h>

// Define number of steps per rotation:
const int angular_units = 2048;

// Wiring:
// Pin 8 to IN1 on the ULN2003 driver
// Pin 9 to IN2 on the ULN2003 driver
// Pin 10 to IN3 on the ULN2003 driver
// Pin 11 to IN4 on the ULN2003 driver

// Pin 4 to IN1 on the ULN2003 driver
// Pin 5 to IN2 on the ULN2003 driver
// Pin 6 to IN3 on the ULN2003 driver
// Pin 7 to IN4 on the ULN2003 driver

// Pin 2 to IN1 on the ULN2003 driver
// Pin 3 to IN2 on the ULN2003 driver
// Pin 12 to IN3 on the ULN2003 driver
// Pin 13 to IN4 on the ULN2003 driver

// Create stepper object called 'myStepper', note the pin order:
//pins are such that wires can be inserted corresponding to driver board pins
Stepper stepper1 = Stepper(2048, 8, 10, 9, 11); //The first argument is the resolution of the stepper motor
Stepper stepper2 = Stepper(2048, 4, 6, 5, 7); //The first argument is the resolution of the stepper motor
Stepper stepper3 = Stepper(2048, 3, 12, 2, 13); //9

//AccelStepper stepper1(AccelStepper::FULL4WIRE, 8, 10, 9, 11);
//AccelStepper stepper2(AccelStepper::FULL4WIRE, 4, 6, 5, 7);
//AccelStepper stepper3(AccelStepper::FULL4WIRE, 3, 12, 2, 13);

void setup() {
  // Set the speed to 5 rpm:
  stepper1.setSpeed(15);
  stepper2.setSpeed(15);
  stepper3.setSpeed(15);
  Serial.begin(9600);
}

void loop() {
  Serial.println("clockwise"); //out
  stepper1.step(-angular_units * 3); //how many steps to move

  Serial.println("counterclockclockwise"); //in
  stepper1.step(angular_units * 3);

  Serial.println("clockwise"); //out
  stepper2.step(-angular_units * 3); //how many steps to move

  Serial.println("counterclockclockwise"); //in
  stepper2.step(angular_units * 3);

  Serial.println("clockwise"); //out
  stepper3.step(-angular_units * 3); //how many steps to move

  Serial.println("counterclockclockwise"); //in
  stepper3.step(angular_units * 3);
}

/* new, non-functional
void setup() {
  // Set the speed to 15 RPM (steps per second is speed multiplied by steps per revolution divided by 60)
  stepper1.setMaxSpeed(100);
  stepper2.setMaxSpeed(100);
  stepper3.setMaxSpeed(100);
  
  Serial.begin(9600);
}

void loop() {
  // Run stepper1
  Serial.println("clockwise"); // out
  stepper1.moveTo(-angular_units * 3);
  while (stepper1.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }

  Serial.println("counterclockwise"); // in
  stepper1.moveTo(angular_units * 3);
  while (stepper1.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }

  // Run stepper2
  Serial.println("clockwise"); // out
  stepper2.moveTo(-angular_units * 3);
  while (stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }

  Serial.println("counterclockwise"); // in
  stepper2.moveTo(angular_units * 3);
  while (stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }

  // Run stepper3
  Serial.println("clockwise"); // out
  stepper3.moveTo(-angular_units * 3);
  while (stepper3.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }

  Serial.println("counterclockwise"); // in
  stepper3.moveTo(angular_units * 3);
  while (stepper3.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
    stepper3.run();
  }
}
*/



