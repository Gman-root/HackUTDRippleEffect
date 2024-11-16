# Load and clean the well data, ensuring it is ready for analysis and model training.

import pandas as pd
import os

def clean_csv(file_path, impute=False):
    df = pd.read_csv(file_path)
    if impute:
        cleaned_df = df.fillna(method='ffill')
    else:
        cleaned_df = df.dropna()
    cleaned_file_path = file_path.replace("raw data", "cleaned data")
    os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
    cleaned_df.to_csv(cleaned_file_path, index=False)

def clean_all_csvs(directory, impute=False):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            clean_csv(file_path, impute)

if __name__ == "__main__":
    raw_data_directory = "/raw data"
    clean_all_csvs(raw_data_directory, impute=True)