import pandas as pd
from io import StringIO

def clean_csv_data(csv_content):
    try:
        print("Cleaning CSV content")

        # Use chunks for large CSV files
        chunk_size = 100000
        csv_stream = StringIO()
        is_header_written = False

        for chunk in pd.read_csv(StringIO(csv_content), chunksize=chunk_size):
            # Ensure required columns exist
            required_columns = [
                'Time', 
                'Inj Gas Meter Volume Instantaneous', 
                'Inj Gas Meter Volume Setpoint', 
                'Inj Gas Valve Percent Open'
            ]

            missing_columns = [col for col in required_columns if col not in chunk.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

            # Forward-fill missing values
            chunk.ffill(inplace=True)

            chunk.fillna(method='bfill', inplace=True)

            # Handle zero or missing values in 'Inj Gas Valve Percent Open'
            chunk['Inj Gas Valve Percent Open'] = chunk['Inj Gas Valve Percent Open'].replace(0, pd.NA).fillna(method='ffill')

            # Calculate deviation and ratio with zero division handling
            chunk['deviation'] = chunk['Inj Gas Meter Volume Instantaneous'] - chunk['Inj Gas Meter Volume Setpoint']
            chunk['ratio'] = chunk['Inj Gas Meter Volume Instantaneous'] / chunk['Inj Gas Valve Percent Open']
            chunk['ratio'].fillna(0, inplace=True)



            # Reorder columns and write to the CSV stream
            columns_order = [
                'Time', 
                'Inj Gas Meter Volume Instantaneous', 
                'Inj Gas Meter Volume Setpoint', 
                'Inj Gas Valve Percent Open', 
                'deviation', 
                'ratio'
            ]
            chunk = chunk[columns_order]

            # Write header only once
            chunk.to_csv(csv_stream, index=False, header=not is_header_written)
            is_header_written = True

        csv_stream.seek(0)  # Reset stream pointer to the beginning
        return csv_stream

    except Exception as e:
        print(f"Failed to clean CSV content: {e}")
        raise