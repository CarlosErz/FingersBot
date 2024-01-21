#include <Servo.h>

Servo S1; // Gordo
Servo S2; // Pinky y Anular agrupados
Servo S3; // Medio e Índice agrupados

int Serv1 = 7;
int Serv2 = 8;
int Serv3 = 9;

int targetPos1 = 0;
int targetPos2 = 0;
int targetPos3 = 0;

int currentPos1 = 0;
int currentPos2 = 0;
int currentPos3 = 0;

int step = 1;
int stepDelay = 2; // Tiempo de retardo entre pasos

void setup() {
  Serial.begin(9600);
  S1.attach(Serv1);
  S2.attach(Serv2);
  S3.attach(Serv3);
}

void loop() {
  if (Serial.available() >= 5) {
    char data[5];
    Serial.readBytes(data, 5);

    // Interpretar la cadena de caracteres
    int gordo = data[0] - '0';
    int pinky = data[1] - '0';
    int medio = data[2] - '0';
    int indice = data[3] - '0';
    int anular = data[4] - '0';

    // Realizar acciones según el estado de cada dedo
    if (gordo == 1) {
      targetPos1 = 180;
    } else {
      targetPos1 = 0;
    }

    // Agrupar Pinky y Anular
    if (pinky == 1 || anular == 1) {
      targetPos2 = 180;
    } else {
      targetPos2 = 0;
    }

    // Agrupar Medio e Índice
    if (medio == 1 || indice == 1) {
      targetPos3 = 180;
    } else {
      targetPos3 = 0;
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
}
