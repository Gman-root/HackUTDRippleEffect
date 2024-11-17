from flask import Flask, request, jsonify
import os
import psycopg2
from training_data.clean_data import clean_csv_data

app = Flask(__name__)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    try:
        # Read the CSV content
        csv_content = file.read().decode('utf-8')
        
        # Clean the CSV data
        cleaned_data = clean_csv_data(csv_content)
        
        # Store the cleaned data in PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv('DB3_NAME'),
            user=os.getenv('DB3_USER'),
            password=os.getenv('DB3_PASS'),
            # local host
            host=os.getenv('DB3_HOST', 'localhost'),
            port=os.getenv('DB3_PORT', '5432')
        )
        cur = conn.cursor()
        for row in cleaned_data:
            cur.execute(
                "INSERT INTO cleaned_data (time, volume_instantaneous, volume_setpoint, valve_percent_open, deviation, ratio) VALUES (%s, %s, %s, %s, %s, %s)",
                row
            )
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": f"Successfully cleaned and saved: {file.filename}"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to clean {file.filename}: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
