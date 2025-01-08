/*
  Arduino code for the Raspberry Pi RTI Microscope

  Written by Ruben Koudijs
*/

#include <AccelStepper.h>
#include <FastLED.h>

// //pin numbers perfboard
// #define EN 4
// #define MS1 8
// #define MS2 9
// #define MS3 10
// #define X_dir 12
// #define Y_dir 3
// #define Z_dir 6
// #define X_step 11
// #define Y_step 2
// #define Z_step 5


//pin numbers pcb
#define LED_PIN 17
#define EN 8
#define MS1 9
#define MS2 10
#define MS3 11

#define X_dir 3
#define Y_dir 5
#define Z_dir 6

#define X_step 2
#define Y_step 4
#define Z_step 7

//lighting constants
#define NUM_LEDS 24
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

//mechatronics constants
#define ms 8
#define motor_speed 500
#define motor_accel 20000
#define Z_motor_speed 500
#define Z_motor_accel 10000
#define lim_X 65000
#define lim_Y 65000
#define lim_Z 100000

int AF_steps = 1000;
int AF_fine_steps = 125;
float speed = 1;
float prev_blur = 0;
byte AF_counter = 0;
byte LED_b = 255;
byte LED_c[] = {255, 255, 80};
bool calibrated = false;

//initialise leds
CRGB leds[NUM_LEDS];

//initialise steppers
AccelStepper X_Motor(1, X_dir, X_step);
AccelStepper Y_Motor(1, Y_dir, Y_step);
AccelStepper Z_Motor(1, Z_dir, Z_step);


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  init_steppers(speed);
  init_leds();
}

void loop() {
  fetchCommand();
  handleMotors();
}

void fetchCommand() {
  if (Serial.available()) {
    String inputString = Serial.readStringUntil("/n");
    inputString.trim();
    executeCommand(inputString);
  }
}

void executeCommand(String command) {
  if (command == "XS") {
    X_Motor.stop();

  } else if (command == "YS") {
    Y_Motor.stop();

  } else if (command == "ZS") {
    Z_Motor.stop();

  } else if (command == "X+") {
    digitalWrite(EN, LOW);
    X_Motor.moveTo(lim_X);

  } else if (command == "X-") {
    digitalWrite(EN, LOW);
    if (calibrated) {
      X_Motor.moveTo(0);
    } else {
      X_Motor.moveTo(-lim_X);
    }

  } else if (command == "Y+") {
    digitalWrite(EN, LOW);
    Y_Motor.moveTo(lim_Y);

  } else if (command == "Y-") {
    digitalWrite(EN, LOW);
    if (calibrated) {
      Y_Motor.moveTo(0);
    } else {
      Y_Motor.moveTo(-lim_Y);
    }

  } else if (command == "Z+") {
    digitalWrite(18, HIGH);
    Z_Motor.moveTo(lim_Z);

  } else if (command == "Z-") {
    digitalWrite(18, HIGH);
    Z_Motor.moveTo(- lim_Z);

  } else if (command == "Z0") {
    digitalWrite(EN, LOW);
    Z_Motor.moveTo(0);

  } else if (command == "Z remove") {
    Z_Motor.setMaxSpeed(3 * Z_motor_speed);
    digitalWrite(EN, LOW);
    digitalWrite(18, HIGH);
    Z_Motor.setSpeed(-1000);
    while (true) {
      Z_Motor.runSpeed();
    }

  } else if (command == "Z insert") {
    Z_Motor.setMaxSpeed(3 * Z_motor_speed);
    digitalWrite(EN, LOW);
    digitalWrite(18, HIGH);
    Z_Motor.setSpeed(1000);
    while (true) {
      Z_Motor.runSpeed();
    }

  } else if (command == "CAL") {
    calibrate();
    calibrated = true;

  } else if (command == "AFS") {
    AF_steps = 1000;
    AF_counter = 0;
    prev_blur = 0;
  
  } else if (command == "AFF") {
    if (abs(AF_steps) > AF_fine_steps) {
      if (AF_steps < 0){
        AF_steps = - AF_fine_steps;
      } else {
        AF_steps = AF_fine_steps;
      }
    }

  } else if (command.startsWith("AF")) {
    command.remove(0,2);
    autoFocus(command.toFloat());

  } else if (command.startsWith("LED1")) {
    command.remove(0,4);
    setLED(command.toInt(), true);

  } else if (command.startsWith("LED0")) {
    command.remove(0,4);
    setLED(command.toInt(), false);

  } else if (command.startsWith("SPEED")) {
    command.remove(0,5);
    speed = 1/pow(2, command.toInt());
    Serial.print(" speed: ");
    Serial.println(speed);
    init_steppers(speed);

  } else if (command.startsWith("SP1")) {
    command.remove(0,3);
    int distance = - (lim_X / 65) * command.toInt();
    stereoPhotography(distance, false);

  } else if (command.startsWith("SP2")) {
    command.remove(0,3);
    int distance = 2 * (lim_X / 65) * command.toInt();
    stereoPhotography(distance, true);
    
  } else if (command.startsWith("FS")){
    command.remove(0,2);
    focusStack(command.toFloat());

  } else if (command.startsWith("LED_B")) {
    command.remove(0,5);
    LED_b = command.toInt();
    init_leds();

  } else if (command.startsWith("LED_C")) {
    command.remove(0,5);
    LED_c[0] = command.substring(0,3).toInt();
    LED_c[1] = command.substring(3,6).toInt();
    LED_c[2] = command.substring(6,9).toInt();
    init_leds();

  } else if (command == "test LED"){
    test_leds();

  } else if (command == "blink") {
    while (1) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
      digitalWrite(LED_BUILTIN, LOW);
      delay(1000);
    }
  }
}


