from flask import Flask, request, jsonify
import os
import psycopg2
from io import StringIO
from training_data.clean_data import clean_csv_data
import socket

app = Flask(__name__)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    try:
        # Read CSV content
        csv_content = file.read().decode('utf-8')
        
        # Clean the CSV data
        cleaned_csv_stream = clean_csv_data(csv_content)
        
        # Database connection setup
        db_params = {
            "dbname": os.getenv('DB3_NAME'),
            "user": os.getenv('DB3_USER'),
            "password": os.getenv('DB3_PASS'),
            "host": os.getenv('DB3_HOST', 'localhost'),
            "port": os.getenv('DB3_PORT', '5432')
        }
        
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Copy the cleaned CSV data into PostgreSQL using the COPY command
                cur.copy_expert(
                    sql="""
                        COPY cleaned_data (time, volume_instantaneous, volume_setpoint,
                        valve_percent_open, deviation, ratio)
                        FROM STDIN WITH CSV HEADER
                    """,
                    file=cleaned_csv_stream
                )
            conn.commit()
        
        return jsonify({"message": f"Successfully cleaned and saved: {file.filename}"}), 200

    except psycopg2.DatabaseError as db_err:
        return jsonify({"message": f"Database error: {db_err}"}), 500
    except UnicodeDecodeError:
        return jsonify({"message": "File encoding not supported. Please use UTF-8 encoding."}), 400
    except Exception as e:
        return jsonify({"message": f"Failed to clean {file.filename}: {e}"}), 500

if __name__ == "__main__":
    # Get the machine's IP address dynamically
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    app.run(debug=True, host=local_ip, port=5000)  # Run on machine's IP address