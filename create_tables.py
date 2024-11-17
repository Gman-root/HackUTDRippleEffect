import os
import psycopg2

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS cleaned_data (
            id SERIAL PRIMARY KEY,
            time TIMESTAMP NOT NULL,
            volume_instantaneous FLOAT NOT NULL,
            volume_setpoint FLOAT NOT NULL,
            valve_percent_open FLOAT NOT NULL,
            deviation FLOAT NOT NULL,
            ratio FLOAT NOT NULL
        )
        """,
    )
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB3_NAME'),
            user=os.getenv('DB3_USER'),
            password=os.getenv('DB3_PASS'),
            host=os.getenv('DB3_HOST', 'localhost'),
            port=os.getenv('DB3_PORT', '5432')
        )
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except Exception as error:
        print(f"Error creating tables: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
