#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

/* WiFi Credentials */
const char* ssid = "SUNBEAM";
const char* password = "1234567890";

/* MQTT Broker */
const char* mqtt_server = "172.18.4.147";  // Your PC IP
const int mqtt_port = 1883;
const char* topic = "environment/data";

/* Sensor Pins */
#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

/* -------------------- */
void connectWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

/* -------------------- */
void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT... ");
    if (client.connect("ESP32_ENV")) {
      Serial.println("Connected");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 2 sec");
      delay(2000);
    }
  }
}

/* -------------------- */
void setup() {
  Serial.begin(115200);
  dht.begin();

  connectWiFi();

  client.setServer(mqtt_server, mqtt_port);
}

/* -------------------- */
void loop() {
  if (!client.connected()) {
    connectMQTT();
  }

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gas = analogRead(MQ2_PIN);

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed");
    return;
  }

  String payload = String(temp) + "," + String(hum) + "," + String(gas);

  client.publish(topic, payload.c_str());
  Serial.println("Published: " + payload);

  delay(3000);
}
