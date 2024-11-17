import pandas as pd
import os

def detect_hydrate(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Calculate absolute deviation
        df['absolute_deviation'] = df['deviation'].abs()
        
        # Optionally, use a rolling window approach for dynamic thresholds
        window_size = 100  
        df['rolling_ratio_95'] = df['ratio'].rolling(window=window_size).quantile(0.95)
        df['rolling_ratio_05'] = df['ratio'].rolling(window=window_size).quantile(0.05)
        df['rolling_dev_95'] = df['absolute_deviation'].rolling(window=window_size).quantile(0.95)
        
        df['train_flag'] = ((df['ratio'] > df['rolling_ratio_95']) | 
                            (df['ratio'] < df['rolling_ratio_05']) | 
                            (df['absolute_deviation'] > df['rolling_dev_95']) |
                            (df['Inj Gas Valve Percent Open'] > 90))
        
        # Drop intermediate columns if not needed
        df.drop(columns=['absolute_deviation', 'rolling_ratio_95', 'rolling_ratio_05', 'rolling_dev_95'], inplace=True)
        
        # Save the data with train_flag
        train_file_path = file_path.replace("cleaned data", "train data")
        os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
        df.to_csv(train_file_path, index=False)
        print(f"Successfully processed and saved: {train_file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def process_all_csvs(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            detect_hydrate(file_path)

def main():
    cleaned_data_directory = os.path.join(os.path.dirname(__file__), "../cleaned data")
    process_all_csvs(cleaned_data_directory)

if __name__ == "__main__":
    main()
