#include <Wire.h>

// I2C address of the NodeMCU
#define I2C_ADDRESS 0x12

int dataToSend = 42;  // Sample data to be sent
int reading = 250;

void setup() {
  Wire.begin(I2C_ADDRESS);  // Initialize I2C with the NodeMCU's address
  Wire.onRequest(requestEvent);     // Register the onRequest event handler
  pinMode(A0,INPUT);
  Serial.begin(115200);
}

void loop() {
  reading = analogRead(A0);
  reading = map(reading,150,800,0,255);
  Serial.println(reading);
}

void requestEvent() {
  Wire.write(reading);
}