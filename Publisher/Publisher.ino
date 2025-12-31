#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34

const char* ssid = "AndroidAP_5063";
const char* password = "anaghaaa";

const char* broker = "10.223.1.61";
int port = 1883;
const char* topic = "environment/data";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  dht.begin();
  pinMode(MQ2_PIN, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  Serial.print("Connecting to MQTT...");
  while (!mqttClient.connect(broker, port)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("CONNECTED to MQTT");
}

void loop() {
  mqttClient.poll();   // ⭐ REQUIRED ⭐

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();
  int gas    = analogRead(MQ2_PIN);

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT11 read failed");
    delay(2000);
    return;
  }

  String payload = String(temp) + "," + String(hum) + "," + String(gas);

  mqttClient.beginMessage(topic);
  mqttClient.print(payload);
  mqttClient.endMessage();

  Serial.println("Published → " + payload);
  delay(5000);
}
