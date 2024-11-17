import pandas as pd
import os

def clean_csv(file_path):
    try:
        print(f"Cleaning file: {file_path}")
        df = pd.read_csv(file_path)
        
        # Set the first row's 'Inj Gas Meter Volume Setpoint' value
        if 'Inj Gas Meter Volume Setpoint' in df.columns:
            df.at[0, 'Inj Gas Meter Volume Setpoint'] = df['Inj Gas Meter Volume Setpoint'].iloc[0]
        
        # Forward-fill missing values
        df.ffill(inplace=True)
        
        # Calculate the deviation from the setpoint
        df['deviation'] = df['Inj Gas Meter Volume Instantaneous'] - df['Inj Gas Meter Volume Setpoint']
        
        # Calculate the ratio of Inj Gas Meter Volume Instantaneous to Inj Gas Valve Percent Open
        df['ratio'] = df['Inj Gas Meter Volume Instantaneous'] / df['Inj Gas Valve Percent Open']
        
        # Reorder columns
        columns_order = ['Time', 'Inj Gas Meter Volume Instantaneous', 'Inj Gas Meter Volume Setpoint', 
                         'Inj Gas Valve Percent Open', 'deviation', 'ratio']
        df = df[columns_order]
        
        # Save the cleaned data
        cleaned_file_path = file_path.replace("raw data", "cleaned data")
        os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
        df.to_csv(cleaned_file_path, index=False)
        print(f"Successfully cleaned and saved: {cleaned_file_path}")
    except FileNotFoundError as fnfe:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Failed to clean {file_path}: {e}")

def clean_all_csvs(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    print(f"Cleaning all CSV files in directory: {directory}")
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)

def main():
    raw_data_directory = os.path.join(os.path.dirname(__file__), "../raw data")
    print(f"Starting cleaning process for directory: {raw_data_directory}")
    clean_all_csvs(raw_data_directory)
    print("Cleaning process completed.")

if __name__ == "__main__":
    main()