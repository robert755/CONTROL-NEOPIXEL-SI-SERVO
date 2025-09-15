#include <Adafruit_NeoPixel.h>
#include <Servo.h>

#define LED_PIN 6      // Pinul pentru NeoPixel Ring
#define NUM_LEDS 16    // Numărul de LED-uri din NeoPixel Ring

#define OUT1 10        // Ieșirile pentru cele 3 butoane
#define OUT2 9
#define OUT3 8

#define SERVO_PIN 7    // Pinul pentru servomotor

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
Servo myServo;

int currentMode = 1; // Pornire în primul mod
int lastStates[3] = {LOW, LOW, LOW}; // Stările anterioare ale butoanelor

int servoPos = 0;          // Poziția curentă a servomotorului
int servoDirection = 1;    // Direcția de rotație (1 = înainte, -1 = înapoi)
const int servoSpeed = 15; // Viteza de mișcare a servomotorului (în ms)
unsigned long lastServoTime = 0; // Timpul ultimei actualizări a servomotorului

void setup() {
  strip.begin();
  strip.show(); // Inițializează LED-urile
  
  pinMode(OUT1, INPUT);
  pinMode(OUT2, INPUT);
  pinMode(OUT3, INPUT);
  
  myServo.attach(SERVO_PIN); // Atașează servomotorul la pinul specificat
  myServo.write(servoPos); // Setează servomotorul la poziția de start

  staticColor(255, 0, 0); // Pornește cu primul mod (roșu)

  Serial.begin(9600); // Inițializează comunicarea serială
}

void loop() {
  // Citește comenzile trimise prin serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Citește comanda completă
    if (command == "red") {
      staticColor(255, 0, 0); // Roșu
    } else if (command == "green") {
      staticColor(0, 255, 0); // Verde
    } else if (command == "blue") {
      staticColor(0, 0, 255); // Albastru
    } else if (command == "left") {
      moveServo(-1); // Mișcă servo la stânga
    } else if (command == "right") {
      moveServo(1); // Mișcă servo la dreapta
    }
  }

  // Actualizează mișcarea continuă a servomotorului
  if (millis() - lastServoTime >= servoSpeed) {
    moveServo(servoDirection);
    lastServoTime = millis();
  }
}

void moveServo(int direction) {
  servoPos += direction;
  if (servoPos >= 180 || servoPos <= 0) {
    servoDirection = -servoDirection; // Schimbă direcția la limită
  }
  myServo.write(servoPos);
}

void staticColor(int r, int g, int b) {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(r, g, b));
  }
  strip.show();
}
