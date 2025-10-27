#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }
  if (!mpu.begin()) {
    Serial.println(F("MPU6050 non detecte"));
    while (1) { delay(10); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println(F("MPU6050 pret"));
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  Serial.print(F("Ax=")); Serial.print(a.acceleration.x);
  Serial.print(F(" Ay=")); Serial.print(a.acceleration.y);
  Serial.print(F(" Az=")); Serial.print(a.acceleration.z);
  Serial.print(F(" | Gz=")); Serial.print(g.gyro.z);
  Serial.println(F(" (SI units)"));
  delay(200);
}
