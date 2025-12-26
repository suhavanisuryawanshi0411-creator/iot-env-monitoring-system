from flask import Flask, render_template, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
db_config = {
    'user': 'root',
    'password': 'root', 
    'host': 'localhost',
    'database': 'smart_env'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    """Get the single most recent reading."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/api/history')
def get_history():
    """Get the last 20 readings for the chart."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Get last 20 records, then reverse them so the chart is Left-to-Right (Oldest -> Newest)
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    data = list(reversed(rows))
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible from other computers on your network
    app.run(host='0.0.0.0', port=5000, debug=True)