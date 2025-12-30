import requests
import paho.mqtt.client as mqtt

API_KEY = "PTQYSGQUES6Q5EI6"

def on_message(client, userdata, msg):
    temp, hum, gas = msg.payload.decode().split(",")

    url = "https://api.thingspeak.com/update"
    payload = {
        "api_key": PTQYSGQUES6Q5EI6,
        "field1": temp,
        "field2": hum,
        "field3": gas
    }

    r = requests.get(url, params=payload)
    print("ThingSpeak Update:", r.text)

client = mqtt.Client()
client.on_message = on_message
client.connect("10.154.102.60", 1883)
client.subscribe("environment/data")
client.loop_forever()
