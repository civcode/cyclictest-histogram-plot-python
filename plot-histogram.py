#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def plot_core_values(csv_file, title, save, filename):
    # Reading the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Convert the core columns to numeric
    data[['core1', 'core2', 'core3', 'core4']] = data[['core1', 'core2', 'core3', 'core4']].apply(pd.to_numeric)
    data['time'] = data['time'].apply(pd.to_numeric)

    # Convert the time and core columns to numpy arrays
    time = data['time'].to_numpy()
    core1 = data['core1'].to_numpy()
    core2 = data['core2'].to_numpy()
    core3 = data['core3'].to_numpy()
    core4 = data['core4'].to_numpy()

    # Plotting the values of all cores over time with a logarithmic y-axis
    plt.figure(figsize=(12, 8))

    plt.plot(time, core1, label='core1')
    plt.plot(time, core2, label='core2')
    plt.plot(time, core3, label='core3')
    plt.plot(time, core4, label='core4')

    plt.yscale('log')
    plt.xlabel('Latency in µs')
    plt.ylabel('Count')
    plt.title(title)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    if save:
        plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot histogram from a CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--title', type=str, default='', help='Title of the plot')
    parser.add_argument('--save', action='store_true', help='Save the plot to a file')
    parser.add_argument('--filename', type=str, default='plot.png', help='Name of the output file')

    args = parser.parse_args()
    plot_core_values(args.csv_file, args.title, args.save, args.filename)

