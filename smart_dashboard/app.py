from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="env_monitoring"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT temperature, humidity, gas, timestamp
        FROM sensor_data
        ORDER BY id DESC LIMIT 20
    """)
    data = cursor.fetchall()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)