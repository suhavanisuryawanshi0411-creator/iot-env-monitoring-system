#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include <DHT.h>

const char* ssid = "SUNBEAM";
const char* password = "1234567890";

const char* broker = "172.18.3.9";  
int port = 1883;
const char* topic = "environment/data";

#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34

DHT dht(DHTPIN, DHTTYPE);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");
  
  // Connect to MQTT Broker (Added a loop to retry until connected)
  Serial.print("Connecting to MQTT Broker...");
  while (!mqttClient.connect(broker, port)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("Connected to MQTT Broker");
}

void loop() {
  // Ensure MQTT stays connected
  mqttClient.poll();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int gasValue = analogRead(MQ2_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  // Create message string
  String data = String(temperature) + "," + String(humidity) + "," + String(gasValue);

  // Publish data to MQTT
  mqttClient.beginMessage(topic);
  mqttClient.print(data);
  mqttClient.endMessage();

  // Print to Serial Monitor (This is where you see it!)
  Serial.print("Data Sent to Serial: ");
  Serial.println(data);

  delay(3000);  // send every 3 seconds
}