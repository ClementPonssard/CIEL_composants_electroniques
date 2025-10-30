void setup() {
  // Setup serial communication at baudrate 9600 for reading the light sensor
  Serial.begin(9600);
}

void loop() {
  // reads the input on analog pin A0
  int lightValue = analogRead(A0);

  // Print out the values to read in the Serial Monitor
  Serial.print("Analog reading (0-1023): ");
  Serial.print(lightValue);

  // Use the value to determine how dark it is 
  // (Try tweaking these to make it more accurate)
  if (lightValue < 30) {
    Serial.println(" - Très lumineux");
  } else if (lightValue < 200) {
    Serial.println(" - Lumineux");
  } else if (lightValue < 500) {
    Serial.println(" - Sombre");
  } else if (lightValue < 800) {
    Serial.println(" - Noir");
  } else {
    Serial.println(" - Very bright");
  }

  delay(500);
}