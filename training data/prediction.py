import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from tkinter import Tk
from tkinter import filedialog
from numpy import ndarray


def predictHydrate(filename, directory):
    # Define feature columns and target
    frames = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path, parse_dates=['Time'])
    df['volume_diff'] = df['Inj Gas Meter Volume Setpoint'] - df['Inj Gas Meter Volume Instantaneous']
    df['rate_of_change'] = df['Inj Gas Meter Volume Instantaneous'].diff().fillna(0)

    features = ['Inj Gas Meter Volume Instantaneous', 'Inj Gas Meter Volume Setpoint', 'Inj Gas Valve Percent Open', 'volume_diff', 'rate_of_change']
    target = ['hydrate_flag']
    # Splitting the dataset into training and testing
    X = df[features]
    y = df[target]
    X_train = X
    y_train = y
    unknown = pd.read_csv(filename)
    unknown['volume_diff'] = unknown['Inj Gas Meter Volume Setpoint'] - unknown['Inj Gas Meter Volume Instantaneous']
    unknown['rate_of_change'] = unknown['Inj Gas Meter Volume Instantaneous'].diff().fillna(0)

    X_test = unknown[features]
    y_test = unknown[target]

    # Initializing the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predictions on the test set
    predictions = model.predict(X_test) 
    unknown['hydrate_flag'] =  predictions
    # Evaluate model performance

def main():
    directory = os.path.join(os.path.dirname(__file__), "../train data")
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        predictHydrate(file_path, directory)
        return file_path
    else:
        print("No file selected.")
        return None
    
if __name__ == "__main__":
    main()