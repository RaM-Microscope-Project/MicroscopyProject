#include <AccelStepper.h>
#include <FastLED.h>

// LED strip configuration
#define LED_PIN 14
#define NUM_LEDS 24
#define BRIGHTNESS 255
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

// Define number of steps per revolution for the stepper motor
const int stepsPerRevolution = 2048;

//Motor layout when looking at front end of microscope
//1 (A); Top left
//2 (B); Top right
//3 (C); Bottom

// Initialize the first stepper motor on pins 8, 10, 9, 11
AccelStepper stepper1(AccelStepper::FULL4WIRE, 8, 10, 9, 11);

// Initialize the second stepper motor on pins 4, 6, 5, 7
AccelStepper stepper2(AccelStepper::FULL4WIRE, 4, 6, 5, 7);

// Initialize the third stepper motor on pins 2, 13, 3, 12
AccelStepper stepper3(AccelStepper::FULL4WIRE, 2, 13, 3, 12);

long targetPos1 = 0;
long targetPos2 = 0;
long targetPos3 = 0;

String inputString = "";      // A string to hold incoming data
bool stringComplete = false;  // Whether the string is complete

void setup() {
  // LED setup
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);

  // Turn off all LEDs at the start
  FastLED.clear();
  FastLED.show();

  Serial.begin(9600);

  // Set maximum speed and acceleration for each motor
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(5000);

  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(5000);

  stepper3.setMaxSpeed(1000);
  stepper3.setAcceleration(5000);

  // Debug test if motors run at all
  // stepper1.setSpeed(500);
  // stepper2.setSpeed(500);
  // stepper3.setSpeed(500);
  stepper1.speed();
}

void loop() {
  inputToString();

  // Process the input string when it's complete
  if (stringComplete) {
    int ledIndex = inputString.toInt() - 1;  // Convert the string to an integer and adjust for 0-based index

    if (ledIndex >= 0 && ledIndex < NUM_LEDS) {  // Ensure the index is valid
      Serial.print("LED index is ");
      Serial.println(ledIndex);
      toggleLED(ledIndex, CRGB(255, 255, 20));  // warm white
    }

    else if (inputString == "d") {
      Serial.println("Key D pressed. Moving motors...");
      // Move stepper1 clockwise and stepper2 counterclockwise
      toggleMotor(stepper1, 500);
      toggleMotor(stepper2, -500);
      stepper3.setSpeed(0);
    }
    else if (inputString == "a") {
      Serial.println("Key A pressed. Moving motors...");
      // Move stepper1 counterclockwise and stepper2 clockwise
      toggleMotor(stepper1, -500);
      toggleMotor(stepper2, 500);
      stepper3.setSpeed(0);
    }
    else if (inputString == "s") {
      Serial.println("Key S pressed. Moving motors...");
      // Move stepper1 and stepper2 clockwise, stepper3 counterclockwise
      toggleMotor(stepper1, 500);
      toggleMotor(stepper2, 500);
      toggleMotor(stepper3, -500);
    }
    else if (inputString == "w") {
      Serial.println("Key W pressed. Moving motors...");
      // Move stepper1 and stepper2 counterclockwise, stepper3 clockwise
      toggleMotor(stepper1, -500);
      toggleMotor(stepper2, -500);
      toggleMotor(stepper3, 500);
    }
    else if (inputString == "q") {
      Serial.println("Q for Quit. Stopping all motors...");
      // Stop all motors
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }
    else if (inputString == "m") {
      Serial.println("M for Mute. Turning off all LEDs...");
      // Stop all motors
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }


    //Motor debug starts here

    else if (inputString == "i") {
      Serial.println("Motor 1 running anticlockwise...");
      // Move stepper1 anticlockwise
      toggleMotor(stepper1, 500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }
    else if (inputString == "j") {
      Serial.println("Motor 1 running clockwise...");
      // Move stepper1 clockwise
      toggleMotor(stepper1, -500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }
    else if (inputString == "o") {
      Serial.println("Motor 2 running anticlockwise...");
      // Move stepper2 anticlockwise
      stepper1.setSpeed(0);
      toggleMotor(stepper2, 500);
      stepper3.setSpeed(0);
    }
    else if (inputString == "k") {
      Serial.println("Motor 2 running clockwise...");
      // Move stepper2 clockwise
      stepper1.setSpeed(0);
      toggleMotor(stepper2, -500);
      stepper3.setSpeed(0);
    }

    else if (inputString == "p") {
      // Move stepper3 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      toggleMotor(stepper3, 500);
    }

    else if (inputString == "l") {
      // Move stepper3 clockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      toggleMotor(stepper3, -500);
    }

    else {
      Serial.println("Invalid command");
    }

    // Clear the input string
    inputString = "";
    stringComplete = false;
  }

  // Run the motors
  stepper1.runSpeed();
  stepper2.runSpeed();
  stepper3.runSpeed();
}

void toggleMotor(AccelStepper &motor, int newSpeed) {
  if (motor.speed() == 0.0) { 
    motor.setSpeed(newSpeed);
  }
  else { //if motor not spinning
    motor.setSpeed(0);  //stop
  }

  Serial.println("call");
}

void toggleLED(int ledIndex, CRGB color) {
  if (leds[ledIndex] == CRGB::Black) {
    leds[ledIndex] = color;  // Set LED to warm white
  } else {
    leds[ledIndex] = CRGB::Black;  // Turn off LED
  }
  FastLED.show();
}

void moveStage() {
  Serial.println("moving stage...");
}

void controlLEDs() {
  Serial.println("controlling LEDs...");
}

void inputToString() {
  // Check for serial input
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {  // Check for the newline character
      stringComplete = true;
      break;
    } else {
      inputString += inChar;  // Add the character to the input string
    }
  }
}
