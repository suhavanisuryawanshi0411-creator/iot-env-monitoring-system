import paho.mqtt.client as mqtt
import mysql.connector

db = mysql.connector.connect(
    host="10.223.1.61",
    user="root",
    password="root",
    database="env_monitoring"
)
cursor = db.cursor()

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print("Received:", data)

    temp, hum, gas = data.split(',')

    sql = """
    INSERT INTO sensor_data (temperature, humidity, gas)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (temp, hum, gas))
    db.commit()

    print("Inserted:", temp, hum, gas)

client = mqtt.Client()
client.on_message = on_message

client.connect("10.223.1.61", 1883)
client.subscribe("environment/data")

print("Subscriber running...")
client.loop_forever()