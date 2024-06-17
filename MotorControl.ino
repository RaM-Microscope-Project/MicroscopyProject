#include <AccelStepper.h>
#include <FastLED.h>

// LED strip configuration
#define LED_PIN 14
#define NUM_LEDS 6
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

  //debug test if motors run at all
  //stepper1.setSpeed(500);
  //stepper2.setSpeed(500);
  //stepper3.setSpeed(500);

  //digitalWrite(A0, HIGH);
}

void loop() {
  // Check for serial input
  if (Serial.available() > 0) {
    char input = Serial.read();
    int ledIndex = 0;

    //Toggle corresponding LED based on key press
    if (input >= '1' && input <= '6') {
      Serial.print("key is ");
      Serial.println(input);
      ledIndex = input - '1';
      //toggleLED(ledIndex, CRGB(255, 255, 50));  //pure white
      toggleLED(ledIndex, CRGB(255, 255, 20));  //warm white
    }

    if (input == 'g'){
      Serial.print("key is ");
      Serial.println(input);
      toggleLED(ledIndex, CRGB(255, 255, 20));  //warm white
    }

    if (input == 'h'){
      Serial.print("key is ");
      Serial.println(input);
      toggleLED(ledIndex, CRGB(255, 255, 20));  //warm white
    }

    if (input == 'd') {
      Serial.println("Key D pressed. Moving motors...");
      // Move stepper1 clockwise and stepper2 counterclockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(0);
    }

    else if (input == 'a') {
      Serial.println("Key A pressed. Moving motors...");
      // Move stepper1 counterclockwise and stepper2 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(500);
      stepper3.setSpeed(0);
    }

    else if (input == 's') {
      Serial.println("Key S pressed. Moving motors...");
      // Move stepper1 and stepper2 clockwise, stepper3 counterclockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(500);
      stepper3.setSpeed(-500);
    }

    else if (input == 'w') {
      Serial.println("Key W pressed. Moving motors...");
      // Move stepper1 and stepper2 counterclockwise, stepper3 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(500);
    }

    else if (input == 'q') {
      Serial.println("Q for Quit. Stopping all motors...");
      // Move stepper1 and stepper2 counterclockwise, stepper3 clockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }

    else if (input == 'i') {
      Serial.println("Motor 1 running...");
      // Move stepper1 anticlockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }

    else if (input == 'j') {
      Serial.println("Motor 1 running...");
      // Move stepper1 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    }

    else if (input == 'o') {
      Serial.println("Motor 2 running...");
      // Move stepper2 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(500);
      stepper3.setSpeed(0);
    }

    else if (input == 'k') {
      Serial.println("Motor 2 running...");
      // Move stepper2 clockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(0);
    }

    else if (input == 'p') {
      Serial.println("Motor 3 running...");
      // Move stepper3 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(500);
    }

    else if (input == 'l') {
      Serial.println("Motor 3 running...");
      // Move stepper3 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(-500);
    }
  }

  stepper1.runSpeed();
  stepper2.runSpeed();
  stepper3.runSpeed();
}

void toggleLED(int ledIndex, CRGB color) {
  if (leds[ledIndex] == CRGB::Black) {
    leds[ledIndex] = color;  // Set LED to warm white
  } else {
    leds[ledIndex] = CRGB::Black;  // Turn off LED
  }
  FastLED.show();
}
