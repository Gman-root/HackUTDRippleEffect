import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def plot_trends(file_path):
    df = pd.read_csv(file_path, parse_dates=['Time'])
    
    # Define set points
    deviation_set_point = 0.0

    # Plot the data
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    fig.suptitle(os.path.basename(file_path), fontsize=16)  # Set the figure title to the CSV file name

    # Plot ratio
    axs[0].plot(df['Time'], df['ratio'], label='Ratio')
    axs[0].scatter(df['Time'][df['train_flag']], df['ratio'][df['train_flag']], color='red', label='Hydrate Flagged')
    axs[0].set_xlabel('Time', fontsize=12)
    axs[0].set_ylabel('Ratio', fontsize=12)
    axs[0].set_title('Ratio Over Time', fontsize=14)
    axs[0].legend()

    # Plot deviation
    axs[1].plot(df['Time'], df['deviation'], label='Deviation')
    axs[1].scatter(df['Time'][df['train_flag']], df['deviation'][df['train_flag']], color='red', label='Hydrate Flagged')
    axs[1].axhline(y=deviation_set_point, color='green', linestyle='--', label='Set Point')
    axs[1].set_xlabel('Time', fontsize=12)
    axs[1].set_ylabel('Deviation', fontsize=12)
    axs[1].set_title('Deviation Over Time', fontsize=14)
    axs[1].legend()

    # Plot Inj Gas Valve Percent Open
    axs[2].plot(df['Time'], df['Inj Gas Valve Percent Open'], label='Inj Gas Valve Percent Open')
    axs[2].scatter(df['Time'][df['train_flag']], df['Inj Gas Valve Percent Open'][df['train_flag']], color='red', label='Hydrate Flagged')
    axs[2].set_xlabel('Time', fontsize=12)
    axs[2].set_ylabel('Inj Gas Valve Percent Open', fontsize=12)
    axs[2].set_title('Inj Gas Valve Percent Open Over Time', fontsize=14)
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the title
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