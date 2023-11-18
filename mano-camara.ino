#include <Servo.h>

Servo S1;
Servo S2;
Servo S3;
Servo S4;
Servo S5;

int Serv1 = 7;
int Serv2 = 8;
int Serv3 = 9;
int Serv4 = 10;
int Servo5 = 11;

int targetPos1 = 0;
int targetPos2 = 0;
int targetPos3 = 0;
int targetPos4 = 0;
int targetPos5 = 0;

int currentPos1 = 0;
int currentPos2 = 0;
int currentPos3 = 0;
int currentPos4 = 0;
int currentPos5 = 0;

int step = 1;
int stepDelay = 2; // Tiempo de retardo entre pasos

void setup() {
  Serial.begin(9600);
  S1.attach(Serv1);
  S2.attach(Serv2);
  S3.attach(Serv3);
  S4.attach(Serv4);
  S5.attach(Servo5);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    Serial.print("Datos recibidos: ");
    Serial.println(data);

    // Implementa el control de transiciones suaves aquí
    if (data == '3') {
      targetPos1 = 180;
    } else if (data == '4') {
      targetPos1 = 0;
    }

    if (data == '5') {
      targetPos2 = 180;
    } else if (data == '6') {
      targetPos2 = 0;
    }

    if (data == '7') {
      targetPos3 = 180;
    } else if (data == '8') {
      targetPos3 = 0;
    }
  }

  // Implementa el control suave de los servos aquí
  if (currentPos1 != targetPos1) {
    if (currentPos1 < targetPos1) {
      currentPos1 += step;
    } else {
      currentPos1 -= step;
    }
    S1.write(currentPos1);
    delay(stepDelay);
  }

  if (currentPos2 != targetPos2) {
    if (currentPos2 < targetPos2) {
      currentPos2 += step;
    } else {
      currentPos2 -= step;
    }
    S2.write(currentPos2);
    delay(stepDelay);
  }

  if (currentPos3 != targetPos3) {
    if (currentPos3 < targetPos3) {
      currentPos3 += step;
    } else {
      currentPos3 -= step;
    }
    S3.write(currentPos3);
    delay(stepDelay);
  }
}

