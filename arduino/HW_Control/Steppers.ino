/*
This file contains the functions for the stepper control
*/

void handleMotors() {
  if ((X_Motor.distanceToGo() == 0)
  && (Z_Motor.distanceToGo() == 0)
  && (Y_Motor.distanceToGo() == 0)) {
    digitalWrite(EN, HIGH);
  } else {
    digitalWrite(EN, LOW);
  }
  X_Motor.run();
  Y_Motor.run();
  Z_Motor.run();
}

void calibrate() {
  init_steppers(1);
  Serial.println("Calibrating");
  delay(500);

  pinMode(17, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
  digitalWrite(4, LOW);

  X_Motor.moveTo(-lim_X);
  Y_Motor.moveTo(-lim_Y);

  Serial.println("Calibrating X");
  while (!digitalRead(17)) {
    X_Motor.run();
  }

  X_Motor.setCurrentPosition(0);
  X_Motor.moveTo(0);
  delay(500);

  Serial.println("Calibrating Y");
  while (!digitalRead(19)) {
    Y_Motor.run();
  }

  Y_Motor.setCurrentPosition(0);
  Y_Motor.moveTo(0);

  Serial.println("Centering");
  XY_Center();
  Z_Motor.setCurrentPosition(0);

  digitalWrite(EN, HIGH);
  init_steppers(speed);
  Serial.println("Done");
}


void XY_Center() {
  digitalWrite(EN, LOW);

  X_Motor.moveTo(lim_X / 2);
  Y_Motor.moveTo(lim_Y / 2);

  while ((X_Motor.distanceToGo() != 0) || (Y_Motor.distanceToGo() != 0)) {
    handleMotors();
  }
  digitalWrite(EN, HIGH);
}


void stereoPhotography(int distance, bool number) {

  if (!calibrated) {
    //calibrate();
    Serial.print("Not calibrated!");
  } 

  digitalWrite(EN, LOW);
  X_Motor.move(distance);

  while (X_Motor.distanceToGo() != 0) {
  handleMotors();
  }
  digitalWrite(EN, HIGH);
}

void focusStack(float h) {
  h *= 200;
  Serial.println(h);
  Z_Motor.move(-h);
}

void autoFocus(float blur) {
  digitalWrite(18, HIGH);
  if ((AF_counter == 0) && (blur < 2.5)){
    AF_steps *= 4;
  }

if ((prev_blur - blur) > 0.10) {
    if (AF_counter == 1){
      AF_steps *= -1;
    } else {
      AF_steps *= -0.5;
    }
  }
  Z_Motor.move(AF_steps);
  prev_blur = blur;
}

void init_steppers(float s) {
  //set stepper values
  X_Motor.setMaxSpeed(s * ms * motor_speed);
  X_Motor.setAcceleration(s * ms * motor_accel);
  X_Motor.setSpeed(s * ms * motor_accel);

  Y_Motor.setMaxSpeed(s * ms * motor_speed);
  Y_Motor.setAcceleration(s * ms * motor_accel);
  Y_Motor.setSpeed(s * ms * motor_speed);

  Z_Motor.setMaxSpeed(Z_motor_speed);
  Z_Motor.setAcceleration(Z_motor_accel);
  Z_Motor.setSpeed(Z_motor_speed);


  //set pinmodes
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT); 
  pinMode(EN, OUTPUT);

  //set microstepping
  if (ms == 1) {
    digitalWrite(MS1, LOW);
    digitalWrite(MS2, LOW);
    digitalWrite(MS3, LOW);
  } else if (ms == 2) {
    digitalWrite(MS1, HIGH);
    digitalWrite(MS2, LOW);
    digitalWrite(MS3, LOW);
  } else if (ms == 4) {
    digitalWrite(MS1, LOW);
    digitalWrite(MS2, HIGH);
    digitalWrite(MS3, LOW);
  } else if (ms == 8) {
    digitalWrite(MS1, HIGH);
    digitalWrite(MS2, HIGH);
    digitalWrite(MS3, LOW);
  } else if (ms == 16) {
    digitalWrite(MS1, HIGH);
    digitalWrite(MS2, HIGH);
    digitalWrite(MS3, HIGH);
  }
  digitalWrite(18, HIGH);

  //disable motors
  digitalWrite(EN, HIGH);
}
