import pandas as pd
import plotly as pt
import os



def detect_hydrate(file_path):
    df = pd.read_csv(file_path)
    df.fillna(method='bfill', inplace=True)
    df.fillna(method='ffill', inplace=True)
    df['Hydrate'] = False
    df.loc[((df['Inj Gas Meter Volume Instantaneous'] < .7*df['Inj Gas Meter Volume Setpoint']) |
    (df['Inj Gas Meter Volume Instantaneous'] < .90*df['Inj Gas Meter Volume Setpoint']) & (df['Inj Gas Valve Percent Open'] > 95)),
    'Hydrate']  = True
    hydrate_flagged_data = file_path.replace("cleaned data", "hydrate flagged data")
    os.makedirs(os.path.dirname(hydrate_flagged_data), exist_ok=True)
    df.to_csv(hydrate_flagged_data, index=False)

   

def detect_all_hydrate(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            detect_hydrate(file_path)


    
def main():
    cleaned_data_directory = os.path.join(os.path.dirname(__file__), "../cleaned data")
    detect_all_hydrate(cleaned_data_directory)

if __name__ == "__main__":
    main()