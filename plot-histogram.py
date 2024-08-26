#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys

def plot_core_values(csv_file, title, save, filename, cpu_list, max_latency):
    # Reading the CSV file into a DataFrame
    data = pd.read_csv(csv_file, delim_whitespace=True, comment='#')

    # Determine the number of CPU columns
    num_cpus = len(data.columns) - 1  # Subtract 1 for the 'time' column

    # Adding a header row dynamically
    columns = ['time'] + [f'cpu{i}' for i in range(num_cpus)]
    data.columns = columns

    # Convert the cpu columns to numeric
    cpu_columns = [f'cpu{i}' for i in range(num_cpus)]
    data[cpu_columns] = data[columns[1:]].apply(pd.to_numeric)
    data['time'] = data['time'].apply(pd.to_numeric)

    # Convert the time and cpu columns to numpy arrays
    time = data['time'].to_numpy()
    cpus = {f'cpu{i}': data[f'cpu{i}'].to_numpy() for i in range(num_cpus)}

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

    # Plotting the values of specified cpus over time with a logarithmic y-axis
    plt.figure(figsize=(12, 8))

    # Plot statistics
    min_latencies = [str(int(x)) for x in min_latencies]
    avg_latencies = [str(int(x)) for x in avg_latencies]
    max_latencies = [str(int(x)) for x in max_latencies]
    table_header = f"cpu_ [min, avg, max]\n"
    text_box = table_header
    for cpu in cpu_list:
        if cpu in cpus:
            i = int(cpu.split('cpu')[1])
            text_box += f"cpu{i}: [{min_latencies[i]}, {avg_latencies[i]}, {max_latencies[i]}] μs\n"

    plt.text(0.5, 0.95, text_box, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', 
             horizontalalignment='center', multialignment='left', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Plot only the specified CPUs
    for cpu in cpu_list:
        if int(cpu.split('cpu')[1]) >= num_cpus:
            print(f"Warning: CPU {cpu} exceeds the number of available CPUs.")
        if cpu in cpus:
            plt.plot(time, cpus[cpu], label=cpu)

    plt.yscale('log')
    plt.xlabel('Latency in µs')
    plt.ylabel('Number of latency samples')
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Set x-axis limit if max_latency is provided
    if max_latency:
        plt.xlim(left=-1, right=max_latency)

    plt.tight_layout()
    if save:
        plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot histogram from a CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--title', type=str, default='', help='Title of the plot')
    parser.add_argument('--save', action='store_true', help='Save the plot to a file')
    parser.add_argument('--filename', type=str, default='', help='Name of the output file. If not set, will be the same as the CSV file')
    parser.add_argument('--cpu-list', type=str, default='', help='Comma-separated list of CPU cores to plot')
    parser.add_argument('--max-latency', type=float, default=None, help='Maximum latency value for the x-axis')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Set the title to the CSV file name if no title is provided
    args.title = args.title if args.title else args.csv_file.split('/')[-1].split('.txt')[0]

    # Set the filename to the CSV file name if no filename is provided
    args.filename = args.filename if args.filename else args.csv_file.split('.txt')[0] + '.png'

    # Parse the CPU list
    cpu_list = [f'cpu{int(cpu)}' for cpu in args.cpu_list.split(',')] if args.cpu_list else [f'cpu{i}' for i in range(num_cpus)]

    plot_core_values(args.csv_file, args.title, args.save, args.filename, cpu_list, args.max_latency)

