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

            # Calculate deviation and ratio with zero division handling
            chunk['deviation'] = chunk['Inj Gas Meter Volume Instantaneous'] - chunk['Inj Gas Meter Volume Setpoint']
            chunk['Inj Gas Valve Percent Open'].replace(0, pd.NA, inplace=True)
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


# Comment out the file reading and saving logic
# def clean_csv(file_path):
#     try:
#         print(f"Cleaning file: {file_path}")
#         df = pd.read_csv(file_path)
#         # ...existing code...
#         cleaned_file_path = file_path.replace("raw data", "cleaned data")
#         os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
#         df.to_csv(cleaned_file_path, index=False)
#         print(f"Successfully cleaned and saved: {cleaned_file_path}")
#     except FileNotFoundError as fnfe:
#         print(f"File not found: {file_path}")
#     except Exception as e:
#         print(f"Failed to clean {file_path}: {e}")

# def clean_all_csvs(directory):
#     if not os.path.exists(directory):
#         print(f"Directory {directory} does not exist.")
#         return
#     print(f"Cleaning all CSV files in directory: {directory}")
#     for filename in os.listdir(directory):
#         if filename.endswith(".csv"):
#             file_path = os.path.join(directory, filename)
#             clean_csv(file_path)

# def main():
#     raw_data_directory = os.path.join(os.path.dirname(__file__), "../raw data")
#     print(f"Starting cleaning process for directory: {raw_data_directory}")
#     clean_all_csvs(raw_data_directory)
#     print("Cleaning process completed.")

# if __name__ == "__main__":
#     main()