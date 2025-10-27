#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println(F("DHT22 example_minimal"));
}

void loop() {
  delay(2000); // DHT22 requires ~2s between reads
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // Celsius

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Erreur lecture DHT22"));
    return;
  }
  Serial.print(F("T="));
  Serial.print(t, 1);
  Serial.print(F("°C  H="));
  Serial.print(h, 1);
  Serial.println(F("%"));
}
