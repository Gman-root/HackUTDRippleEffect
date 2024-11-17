import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def plot_trends(file_path):
    df = pd.read_csv(file_path, parse_dates=['Time'])
    
    # Define set points
    deviation_set_point = 0.0
    inj_gas_meter_volume_set_point = df['Inj Gas Meter Volume Setpoint'].iloc[0]  # Read set point from CSV

    severity_colors = {'high': 'red', 'medium': 'orange', 'none': 'green'}

    # Plot the data
    fig, axs = plt.subplots(4, 1, figsize=(14, 24), constrained_layout=True)  # Adjusted for 4 subplots with constrained layout
    fig.suptitle(os.path.basename(file_path), fontsize=16)  # Set the figure title to the CSV file name

    # Plot ratio
    axs[0].plot(df['Time'], df['ratio'], label='Ratio')
    if 'hydrate_flag' in df.columns:
        for severity in df['severity'].unique():
            severity_df = df[df['severity'] == severity]
            color = severity_colors.get(severity, 'blue')
            axs[0].scatter(severity_df['Time'][severity_df['hydrate_flag']], severity_df['ratio'][severity_df['hydrate_flag']], label=f'Severity: {severity}', color=color)
    axs[0].set_xlabel('Time', fontsize=12)
    axs[0].set_ylabel('Ratio', fontsize=12)
    axs[0].set_title('Ratio Over Time', fontsize=14)
    axs[0].legend(loc='upper right')

    # Plot deviation
    axs[1].plot(df['Time'], df['deviation'], label='Deviation')
    if 'hydrate_flag' in df.columns:
        for severity in df['severity'].unique():
            severity_df = df[df['severity'] == severity]
            color = severity_colors.get(severity, 'blue')
            axs[1].scatter(severity_df['Time'][severity_df['hydrate_flag']], severity_df['deviation'][severity_df['hydrate_flag']], label=f'Severity: {severity}', color=color)
    axs[1].axhline(y=deviation_set_point, color='green', linestyle='--', label='Set Point')
    axs[1].set_xlabel('Time', fontsize=12)
    axs[1].set_ylabel('Deviation', fontsize=12)
    axs[1].set_title('Deviation Over Time', fontsize=14)
    axs[1].legend(loc='upper right')

    # Plot Inj Gas Valve Percent Open
    axs[2].plot(df['Time'], df['Inj Gas Valve Percent Open'], label='Inj Gas Valve Percent Open')
    if 'hydrate_flag' in df.columns:
        for severity in df['severity'].unique():
            severity_df = df[df['severity'] == severity]
            color = severity_colors.get(severity, 'blue')
            axs[2].scatter(severity_df['Time'][severity_df['hydrate_flag']], severity_df['Inj Gas Valve Percent Open'][severity_df['hydrate_flag']], label=f'Severity: {severity}', color=color)
    axs[2].set_xlabel('Time', fontsize=12)
    axs[2].set_ylabel('Valve Percent Open', fontsize=12)
    axs[2].set_title('Inj Gas Valve Percent Open Over Time', fontsize=14)
    axs[2].legend(loc='upper right')

    # Plot Inj Gas Meter Volume Instantaneous
    axs[3].plot(df['Time'], df['Inj Gas Meter Volume Instantaneous'], label='Inj Gas Meter Volume Instantaneous')
    if 'hydrate_flag' in df.columns:
        for severity in df['severity'].unique():
            severity_df = df[df['severity'] == severity]
            color = severity_colors.get(severity, 'blue')
            axs[3].scatter(severity_df['Time'][severity_df['hydrate_flag']], severity_df['Inj Gas Meter Volume Instantaneous'][severity_df['hydrate_flag']], label=f'Severity: {severity}', color=color)
    axs[3].axhline(y=inj_gas_meter_volume_set_point, color='green', linestyle='--', label='Set Point')  # New set point line
    axs[3].set_xlabel('Time', fontsize=12)
    axs[3].set_ylabel('Volume Instantaneous', fontsize=12)
    axs[3].set_title('Inj Gas Meter Volume Instantaneous Over Time', fontsize=14)
    axs[3].legend(loc='upper right')

    plt.show()

def main():
    Tk().withdraw()  # Prevents the Tkinter window from appearing
    file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        plot_trends(file_path)
    else:
        print("No file selected")

if __name__ == "__main__":
    main()
