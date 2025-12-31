from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="env_monitoring"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT temperature, humidity, gas, timestamp
        FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    rows.reverse()   # oldest → newest for graph

    result = []
    for r in rows:
        result.append([
            r[0],                 # temperature
            r[1],                 # humidity
            r[2],                 # gas
            r[3].strftime("%H:%M:%S")  # 🔥 FIXED timestamp
        ])

    db.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
