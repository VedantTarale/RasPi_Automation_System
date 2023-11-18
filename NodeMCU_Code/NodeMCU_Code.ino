#include <Wire.h>

// I2C address of the NodeMCU
#define I2C_ADDRESS 0x12

int reading = 250;

void setup() {
  Wire.begin(I2C_ADDRESS);  // Initialize I2C with the NodeMCU's address
  Wire.onRequest(requestEvent);     // Register the onRequest event handler
  pinMode(A0,INPUT);
}

void loop() {
  reading = analogRead(A0);
  reading = map(reading,10,700,0,255);
  if (reading <= 0) reading = 255;
  delay(500);
}

void requestEvent() {
  Wire.write(reading);
}
