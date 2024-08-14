#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def plot_core_values(csv_file, title, save, filename):
    # Reading the CSV file into a DataFrame
    # data = pd.read_csv(csv_file)
    data = pd.read_csv(csv_file, delim_whitespace=True, comment='#')


    # Adding a header row
    data.columns = ['time', 'core1', 'core2', 'core3', 'core4']

    # Convert the core columns to numeric
    data[['core1', 'core2', 'core3', 'core4']] = data[['core1', 'core2', 'core3', 'core4']].apply(pd.to_numeric)
    data['time'] = data['time'].apply(pd.to_numeric)

    # Convert the time and core columns to numpy arrays
    time = data['time'].to_numpy()
    core1 = data['core1'].to_numpy()
    core2 = data['core2'].to_numpy()
    core3 = data['core3'].to_numpy()
    core4 = data['core4'].to_numpy()

    # Extract the min, avg, and max latencies from the CSV file
    with open(csv_file, 'r') as file:
        lines = file.readlines()

    min_latencies = []
    avg_latencies = []
    max_latencies = []

    for line in lines:
        line = line.strip()
        if line.startswith('# Min'):
            min_latencies = line.split(':')[1].strip().split()
        elif line.startswith('# Avg'):
            avg_latencies = line.split(':')[1].strip().split()
        elif line.startswith('# Max'):
            max_latencies = line.split(':')[1].strip().split()


    # Plotting the values of all cores over time with a logarithmic y-axis
    plt.figure(figsize=(12, 8))

    
    # Plot statistics
    min_latencies = [str(int(x)) for x in min_latencies]
    avg_latencies = [str(int(x)) for x in avg_latencies]
    max_latencies = [str(int(x)) for x in max_latencies]    
    table_header = f"core_ [min, avg, max]\n"
    table_core1 = f"core1: [{min_latencies[0]}, {avg_latencies[0]}, {max_latencies[0]}] μs\n"
    table_core2 = f"core2: [{min_latencies[1]}, {avg_latencies[1]}, {max_latencies[1]}] μs\n"
    table_core3 = f"core3: [{min_latencies[2]}, {avg_latencies[2]}, {max_latencies[2]}] μs\n"
    table_core4 = f"core4: [{min_latencies[3]}, {avg_latencies[3]}, {max_latencies[3]}] μs\n"
    text_box = table_header + table_core1 + table_core2 + table_core3 + table_core4
    plt.text(0.5, 0.95, text_box, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', 
             horizontalalignment='center', multialignment='left', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))


    plt.plot(time, core1, label='core1')
    plt.plot(time, core2, label='core2')
    plt.plot(time, core3, label='core3')
    plt.plot(time, core4, label='core4')

    plt.yscale('log')
    plt.xlabel('Latency in µs')
    plt.ylabel('Number of latency samples')
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

