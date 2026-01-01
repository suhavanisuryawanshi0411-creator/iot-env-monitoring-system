from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

<<<<<<< HEAD
=======
<<<<<<< HEAD
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="env_monitoring"
)
=======
>>>>>>> 5cc7ba934586c300ca8ca8055c6de1c1ad143b23
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="env_monitoring"
    )
<<<<<<< HEAD
=======
>>>>>>> 914a028c453596ec14c268df78fad493481c92da
>>>>>>> 5cc7ba934586c300ca8ca8055c6de1c1ad143b23

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
<<<<<<< HEAD
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
    rows.reverse()  
=======
<<<<<<< HEAD
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
=======
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
>>>>>>> 5cc7ba934586c300ca8ca8055c6de1c1ad143b23

    result = []
    for r in rows:
        result.append([
<<<<<<< HEAD
            r[0],             
            r[1],                
            r[2],                 
            r[3].strftime("%H:%M:%S")  
=======
            r[0],                 # temperature
            r[1],                 # humidity
            r[2],                 # gas
            r[3].strftime("%H:%M:%S")  # 🔥 FIXED timestamp
>>>>>>> 5cc7ba934586c300ca8ca8055c6de1c1ad143b23
        ])

    db.close()
    return jsonify(result)

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> 914a028c453596ec14c268df78fad493481c92da
>>>>>>> 5cc7ba934586c300ca8ca8055c6de1c1ad143b23
