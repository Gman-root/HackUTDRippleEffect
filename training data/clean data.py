import pandas as pd
import os

def clean_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Forward-fill missing values
        df.ffill(inplace=True)
        
        # Calculate the deviation from the setpoint
        df['deviation'] = df['Inj Gas Meter Volume Instantaneous'] - df['Inj Gas Meter Volume Setpoint']
        
        # Reorder columns
        columns_order = ['Time', 'Inj Gas Meter Volume Instantaneous', 'Inj Gas Meter Volume Setpoint', 
                         'Inj Gas Valve Percent Open', 'deviation']
        df = df[columns_order]
        
        # Save the cleaned data
        cleaned_file_path = file_path.replace("raw data", "cleaned data")
        os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
        df.to_csv(cleaned_file_path, index=False)
        print(f"Successfully cleaned and saved: {cleaned_file_path}")
    except Exception as e:
        print(f"Failed to clean {file_path}: {e}")

def clean_all_csvs(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)

def main():
    raw_data_directory = os.path.join(os.path.dirname(__file__), "../raw data")
    clean_all_csvs(raw_data_directory)

if __name__ == "__main__":
    main()