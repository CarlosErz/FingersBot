WINDOWS_SIZE = ("1000x500")
FPS = 60
TITLE = "FINGERS BOT"
ICON_SIZE = ("50x56")
ICON_BLANCO = "img/logo_blanco.ico"
codigo_arduino = """#include <Servo.h>

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
    int indice = data[1] - '0';
    int medio = data[2] - '0';
    int anular = data[3] - '0';
    int pinky = data[4] - '0';

    // Realizar acciones según el estado de cada dedo
    if (gordo == 1) {
        S1.write(0);
    } else {
       S1.write(160);
    }

    // Agrupar Pinky y Anular
    if (pinky == 1 || anular == 1) {
      S2.write(160);
    } else {
      S2.write(0);
    }

    // Agrupar Medio e Índice
    if ( indice == 1  ) {
      S3.write(160);
    } else {
      S3.write(0);
    }
  }
}"""


