/*
  Arduino code for the Raspberry Pi RTI Microscope
  Written for the Pi HAT PCB with Arduino Nano

  By Ruben Koudijs
*/

#include <AccelStepper.h>
// #include <FastLED.h>
#include <Adafruit_NeoPixel.h>

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

//LED dome constants
#define NUM_LEDS 24
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

//mechatronics constants
#define ms 8
#define motor_speed 500
#define motor_accel 20000
#define Z_motor_speed 500
#define Z_motor_accel 10000
#define lim_X 64000
#define lim_Y 64000
#define lim_Z 100000

//code values
int AF_steps = 1000;
int AF_fine_steps = 125;
float speed = 1;
float prev_blur = 0;
byte AF_counter = 0;
byte LED_b = 255;
byte LED_c[] = {255, 255, 80};
bool calibrated = false;

//initialise leds
Adafruit_NeoPixel led_strip = Adafruit_NeoPixel(LED_COUNT, PIN, NEO_RGBW + NEO_KHZ800);

//initialise steppers
AccelStepper X_Motor(1, X_dir, X_step);
AccelStepper Y_Motor(1, Y_dir, Y_step);
AccelStepper Z_Motor(1, Z_dir, Z_step);


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  init_steppers(speed);
  // init_leds();
  led_strip.begin();
}

void loop() {
  fetchCommand();
  handleMotors();
}

void fetchCommand() {
  //this function checks the serial monitor and calls the executeCommand function when a message is recieved
  
  if (Serial.available()) {
    String inputString = Serial.readStringUntil("/n");
    inputString.trim();
    executeCommand(inputString);
  }
}

void executeCommand(String command) {
  //This function recieves commands as a short string and uses if statements to call the appropriate control functions

  //Movement controls:
  
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

//Automated features:
    
  } else if (command == "CAL") {//calibration sequence
    calibrate();
    calibrated = true;

  } else if (command == "AFS") {//stop autofocus mode
    AF_steps = 1000;
    AF_counter = 0;
    prev_blur = 0;
  
  } else if (command == "AFF") {//iteration of autofocus
    if (abs(AF_steps) > AF_fine_steps) {
      if (AF_steps < 0){
        AF_steps = - AF_fine_steps;
      } else {
        AF_steps = AF_fine_steps;
      }
    }

  } else if (command.startsWith("AF")) {//initiate autofocus mode
    command.remove(0,2);
    autoFocus(command.toFloat());

  } else if (command.startsWith("LED1")) {//turn on a LED
    command.remove(0,4);
    setLED(command.toInt(), true);

  } else if (command.startsWith("LED0")) {//turn off a LED
    command.remove(0,4);
    setLED(command.toInt(), false);

  } else if (command.startsWith("SPEED")) {//change speed setting
    command.remove(0,5);
    speed = 1/pow(2, command.toInt());
    Serial.print(" speed: ");
    Serial.println(speed);
    init_steppers(speed);

  } else if (command.startsWith("SP1")) {//first stereo photography capture
    command.remove(0,3);
    int distance = - (lim_X / 20) * command.toInt();
    stereoPhotography(distance, false);

  } else if (command.startsWith("SP2")) {//second stereo photography capture
    command.remove(0,3);
    int distance = 2 * (lim_X / 20) * command.toInt();
    stereoPhotography(distance, true);
    
  } else if (command.startsWith("FS")){//focus stacking
    command.remove(0,2);
    focusStack(command.toFloat());

  } else if (command.startsWith("LED_B")) {//change brightness of LEDs
    command.remove(0,5);
    LED_b = command.toInt();
    init_leds();

//Testing, debugging:
  } else if (command == "Z remove") {//remove the lens arm
    Z_Motor.setMaxSpeed(3 * Z_motor_speed);
    digitalWrite(EN, LOW);
    digitalWrite(18, HIGH);
    Z_Motor.setSpeed(-1000);
    while (true) {
      Z_Motor.runSpeed();
    }

  } else if (command == "Z insert") {//instert the lens arm
    Z_Motor.setMaxSpeed(3 * Z_motor_speed);
    digitalWrite(EN, LOW);
    digitalWrite(18, HIGH);
    Z_Motor.setSpeed(1000);
    while (true) {
      Z_Motor.runSpeed();
    }

  } else if (command.startsWith("LED_C")) {//change the RTI LED color
    command.remove(0,5);
    LED_c[0] = command.substring(0,3).toInt();
    LED_c[1] = command.substring(3,6).toInt();
    LED_c[2] = command.substring(6,9).toInt();
    init_leds();

  } else if (command == "test LED"){//test the RTI dome
    test_leds();

  } else if (command == "blink") {//test the serial communication
    while (1) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
      digitalWrite(LED_BUILTIN, LOW);
      delay(1000);
    }
  }
}


