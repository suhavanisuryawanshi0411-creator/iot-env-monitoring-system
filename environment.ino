#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include <DHT.h>

const char* ssid = "SUNBEAM";
const char* password = "1234567890";


const char* broker = "192.168.1.100";  
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

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");

  // Connect to MQTT Broker
  mqttClient.connect(broker, port);
  Serial.println("Connected to MQTT Broker");
}

// --------------------
void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int gasValue = analogRead(MQ2_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  // Create message
  String data = String(temperature) + "," +
                String(humidity) + "," +
                String(gasValue);

  // Publish data
  mqttClient.beginMessage(topic);
  mqttClient.print(data);
  mqttClient.endMessage();

  Serial.println("Data Sent: " + data);

  delay(3000);  // send every 3 seconds
}
