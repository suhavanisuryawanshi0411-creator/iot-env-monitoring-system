import paho.mqtt.client as mqtt

# -----------------------------
# MQTT Configuration
# -----------------------------
BROKER = "localhost"     # or IP of your MQTT broker
PORT = 1883
TOPIC = "environment/data"

# -----------------------------
# When connected to broker
# -----------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(TOPIC)
        print("📡 Subscribed to topic:", TOPIC)
    else:
        print("❌ Connection failed")

# -----------------------------
# When message is received
# -----------------------------
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print("\nRaw Data:", data)

    try:
        temp, hum, gas = data.split(",")

        print("🌡 Temperature :", temp, "°C")
        print("💧 Humidity    :", hum, "%")
        print("🔥 Gas Level   :", gas)

        if int(gas) > 400:
            print("⚠ WARNING: Gas level HIGH!")

    except:
        print("❌ Invalid data format")

# -----------------------------
# Create MQTT client
# -----------------------------
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# -----------------------------
# Connect to broker
# -----------------------------
print("🔌 Connecting to broker...")
client.connect(BROKER, PORT, 60)

# -----------------------------
# Keep program running
# -----------------------------
client.loop_forever()
