from paho.mqtt import client as mqtt
import mysql.connector
import requests
import time

# ---------- CONFIG ----------
BROKER = "10.223.1.61"
PORT = 1883
TOPIC = "environment/data"

API_KEY = "PTQYSGQUES6Q5EI6"   # ThingSpeak Write API Key

DB_CONFIG = {
    "host": "localhost",
    "user": "root",           # change if needed
    "password": "root",           # your MySQL password
    "database": "env_monitoring"
}
# ----------------------------

# MySQL connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

def upload_to_thingspeak(temp, hum, gas):
    url = "https://api.thingspeak.com/update"
    payload = {
        "api_key": API_KEY,
        "field1": temp,
        "field2": hum,
        "field3": gas
    }
    r = requests.get(url, params=payload)
    print("ThingSpeak response:", r.text)

def save_to_mysql(temp, hum, gas):
    sql = """
        INSERT INTO sensor_data (temperature, humidity, gas)
        VALUES (%s, %s, %s)
    """
    values = (temp, hum, gas)
    cursor.execute(sql, values)
    db.commit()
    print("Saved to MySQL")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print("MQTT connection failed, rc =", rc)

def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode()
        print("Received:", data)

        temp, hum, gas = map(float, data.split(","))

        save_to_mysql(temp, hum, gas)
        upload_to_thingspeak(temp, hum, gas)

        time.sleep(15)  # ThingSpeak rate limit (IMPORTANT)

    except Exception as e:
        print("Error:", e)

# MQTT Client
client = mqtt.Client(client_id="env_monitoring_client")
client.on_connect = on_connect
client.on_message = on_message

<<<<<<< HEAD
client.connect("10.223.1.61", 1883)
client.subscribe("environment/data")

print("Subscriber running...")
client.loop_forever()
=======
client.connect(BROKER, PORT)
client.loop_forever()
>>>>>>> 914a028c453596ec14c268df78fad493481c92da
