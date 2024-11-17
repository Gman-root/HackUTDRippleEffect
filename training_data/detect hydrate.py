import pandas as pd
import os

def detect_hydrate(file_path):
    """
    Detects hydrate formation based on deviations in the data.
    
    Args:
    - file_path (str): Path to the CSV file to process.
    
    Saves:
    - A new CSV file with hydrate flags and severity levels.
    """
    try:
        # Define the date format
        date_format = '%m/%d/%Y %I:%M:%S %p'
        
        # Read the CSV file with the specified date format
        df = pd.read_csv(file_path, parse_dates=['Time'], date_format=date_format)
        df.fillna(method='bfill', inplace=True)
        df.fillna(method='ffill', inplace=True)
        # Check for required columns
        required_columns = ['deviation', 'Inj Gas Valve Percent Open']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        df['hydrate_flag'] = False  # Initialize hydrate_flag to False for all rows
        df['severity'] = 'none'  # Initialize severity to 'low' by default

        # Then apply the conditions for setting the values
        condition = (
            (df['Inj Gas Meter Volume Instantaneous'] < .7 * df['Inj Gas Meter Volume Setpoint']) |
            ((df['Inj Gas Meter Volume Instantaneous'] < .9 * df['Inj Gas Meter Volume Setpoint']) & (df['Inj Gas Valve Percent Open'] > .9))
        )
        df.loc[condition, 'hydrate_flag'] = True
        df.loc[condition, 'severity'] = 'medium'

        # Apply severity for high risk
        high_condition = (
            (df['Inj Gas Meter Volume Instantaneous'] < .5 * df['Inj Gas Meter Volume Setpoint']) |
            ((df['Inj Gas Meter Volume Instantaneous'] < .75 * df['Inj Gas Meter Volume Setpoint']) & (df['Inj Gas Valve Percent Open'] > .9))
        )
        df.loc[high_condition, 'severity'] = 'high'

        # Save the data with hydrate flag and severity
        train_file_path = file_path.replace("cleaned data", "train data")
        os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
        df.to_csv(train_file_path, index=False)
        print(f"Successfully processed and saved: {train_file_path}")
    except ValueError as ve:
        print(f"Value error processing {file_path}: {ve}")
    except FileNotFoundError as fnfe:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def process_all_csvs(directory):
    """
    Processes all CSV files in the given directory and applies hydrate detection.
    
    Args:
    - directory (str): Path to the directory containing the CSV files.
    """
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            detect_hydrate(file_path)

def main():
    # Process all CSV files in the cleaned data directory
    cleaned_data_directory = os.path.join(os.path.dirname(__file__), "../cleaned data")
    process_all_csvs(cleaned_data_directory)

if __name__ == "__main__":
    main()
