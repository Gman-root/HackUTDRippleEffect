import pandas as pd
import os

def process_historical_data(train_directory):
    data_frames = []
    for filename in os.listdir(train_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(train_directory, filename)
            df = pd.read_csv(file_path, parse_dates=['Time'])
            data_frames.append(df)
    if data_frames:
        return pd.concat(data_frames)
    else:
        return pd.DataFrame()

def detect_hydrate(file_path, historical_data=None):
    try:
        # Define the date format
        date_format = '%m/%d/%Y %I:%M:%S %p'
        
        # Read the CSV file with the specified date format
        df = pd.read_csv(file_path, parse_dates=['Time'], date_format=date_format)
        
        # Check for required columns
        required_columns = ['deviation', 'Inj Gas Valve Percent Open']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Initialize new columns
        df['hydrate_flag'] = False
        df['severity'] = 'none'
        
        # Calculate additional contextual features
        df['absolute_deviation'] = df['deviation'].abs()
        df['rate_of_change'] = df['deviation'].diff()
        
        # Rolling window size for oscillation detection
        window_size = 5
        
        # Calculate rolling statistics
        df['rolling_mean'] = df['deviation'].rolling(window=window_size).mean()
        df['rolling_std'] = df['deviation'].rolling(window=window_size).std()
        
        # Dynamic threshold based on historical data
        if historical_data is not None and not historical_data.empty:
            threshold = historical_data['rolling_std'].mean() * 2
        else:
            threshold = 10  # Default threshold if no historical data is available
        
        df['dynamic_threshold'] = threshold
        
        # Initialize state
        hydrate_active = False
        
        for i in range(window_size, len(df)):
            current_deviation = df['deviation'].iloc[i]
            rolling_mean = df['rolling_mean'].iloc[i]
            rolling_std = df['rolling_std'].iloc[i]
            dynamic_threshold = df['dynamic_threshold'].iloc[i]

            # Check for oscillation around the set line
            oscillating = rolling_std < dynamic_threshold
            
            if hydrate_active:
                if oscillating:
                    # Stop hydrate state if oscillation resumes
                    hydrate_active = False
                    df.at[i, 'hydrate_flag'] = False
                    df.at[i, 'severity'] = 'none'
                else:
                    # Maintain hydrate state, update severity
                    df.at[i, 'hydrate_flag'] = True
                    if current_deviation < rolling_mean:
                        df.at[i, 'severity'] = 'high'  # More negative deviation
                    else:
                        df.at[i, 'severity'] = 'medium'  # Recovering
            else:
                if not oscillating and (current_deviation < -dynamic_threshold):
                    # Start hydrate state on a significant spike downward
                    hydrate_active = True
                    df.at[i, 'hydrate_flag'] = True
                    df.at[i, 'severity'] = 'high'
                else:
                    df.at[i, 'hydrate_flag'] = False
                    df.at[i, 'severity'] = 'none'
        
        # Drop intermediate columns if not needed
        df.drop(columns=['absolute_deviation', 'rolling_mean', 'rolling_std', 'dynamic_threshold', 'rate_of_change'], inplace=True)
        
        # Save the data with hydrate flag and severity
        train_file_path = file_path.replace("cleaned data", "train data")
        os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
        df.to_csv(train_file_path, index=False)
        print(f"Successfully processed and saved: {train_file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def process_all_csvs(directory, historical_data=None):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            detect_hydrate(file_path, historical_data)

def main():
    # Load and process historical data
    historical_data_directory = os.path.join(os.path.dirname(__file__), "../train data")
    historical_data = process_historical_data(historical_data_directory)
    
    # Process all CSV files in the cleaned data directory
    cleaned_data_directory = os.path.join(os.path.dirname(__file__), "../cleaned data")
    process_all_csvs(cleaned_data_directory, historical_data=historical_data)

if __name__ == "__main__":
    main()
