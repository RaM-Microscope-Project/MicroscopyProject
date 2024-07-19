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
}

void loop() {
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

  // Process the input string when it's complete
  if (stringComplete) {
    int ledIndex = inputString.toInt() - 1;  // Convert the string to an integer and adjust for 0-based index

    if (ledIndex >= 0 && ledIndex < NUM_LEDS) {  // Ensure the index is valid
      Serial.print("LED index is ");
      Serial.println(ledIndex);
      toggleLED(ledIndex, CRGB(255, 255, 20));  // warm white
    } else if (inputString == "d") {
      Serial.println("Key D pressed. Moving motors...");
      // Move stepper1 clockwise and stepper2 counterclockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(0);
    } else if (inputString == "a") {
      Serial.println("Key A pressed. Moving motors...");
      // Move stepper1 counterclockwise and stepper2 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(500);
      stepper3.setSpeed(0);
    } else if (inputString == "s") {
      Serial.println("Key S pressed. Moving motors...");
      // Move stepper1 and stepper2 clockwise, stepper3 counterclockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(500);
      stepper3.setSpeed(-500);
    } else if (inputString == "w") {
      Serial.println("Key W pressed. Moving motors...");
      // Move stepper1 and stepper2 counterclockwise, stepper3 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(500);
    } else if (inputString == "q") {
      Serial.println("Q for Quit. Stopping all motors...");
      // Stop all motors
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    } else if (inputString == "i") {
      Serial.println("Motor 1 running...");
      // Move stepper1 anticlockwise
      stepper1.setSpeed(500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    } else if (inputString == "j") {
      Serial.println("Motor 1 running...");
      // Move stepper1 clockwise
      stepper1.setSpeed(-500);
      stepper2.setSpeed(0);
      stepper3.setSpeed(0);
    } else if (inputString == "o") {
      Serial.println("Motor 2 running...");
      // Move stepper2 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(500);
      stepper3.setSpeed(0);
    } else if (inputString == "k") {
      Serial.println("Motor 2 running...");
      // Move stepper2 clockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(-500);
      stepper3.setSpeed(0);
    } else if (inputString == "p") {
      Serial.println("Motor 3 running...");
      // Move stepper3 anticlockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(500);
    } else if (inputString == "l") {
      Serial.println("Motor 3 running...");
      // Move stepper3 clockwise
      stepper1.setSpeed(0);
      stepper2.setSpeed(0);
      stepper3.setSpeed(-500);
    } else {
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

void toggleLED(int ledIndex, CRGB color) {
  if (leds[ledIndex] == CRGB::Black) {
    leds[ledIndex] = color;  // Set LED to warm white
  } else {
    leds[ledIndex] = CRGB::Black;  // Turn off LED
  }
  FastLED.show();
}

//Example, command~moveStage~x
void handleMessage(String message) {
  String[] tokens = message.split(ClientProtocol.SEPARATOR);
  if (tokens.length > 0) {
    String command = tokens[0];
    switch (command) {
      case ServerProtocol.HELLO:
        client.receiveHello();
        break;
      case ServerProtocol.LOGIN:
        client.receiveLogin();
        break;
      case ServerProtocol.ALREADY_LOGGED_IN:
        client.receiveAlreadyLoggedIn();
        break;
      case ServerProtocol.LIST:
        List<String> players = new ArrayList<>(Arrays.asList(tokens).subList(1, tokens.length));
        client.receiveList(players);
        break;
      case ServerProtocol.NEW_GAME:
        if (tokens.length > 2) {
          client.receiveNewGame(tokens[1], tokens[2]);
        } else {
          client.sendErrorCommand("no username provided");
        }
        break;
      case ServerProtocol.MOVE:
        if (tokens.length > 1) {
          client.receiveMove(Integer.parseInt(tokens[1]));
          break;
        }
        break;
      case ServerProtocol.GAME_OVER:
        if (tokens.length > 2) {
          client.receiveGameOver(tokens[1], tokens[2]);
        }
        break;
      case ServerProtocol.ERROR:
        client.receiveError();
        break;
      default:
        client.sendErrorCommand("Unknown command: " + command);
        break;
    }
  }
}
