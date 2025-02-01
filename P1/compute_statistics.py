"""
compute_statistics.py

This script computes descriptive statistics (mean, median, mode, variance, and standard deviation)
for a list of text files provided as command-line arguments. Results are displayed on the screen
and saved in StatisticsResults.txt in a tabular format.
"""

import os
import time
import sys
from collections import Counter

def read_file(file_path):
    """Reads the file and returns a list of valid numbers."""
    numbers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                numbers.append(float(line.strip()))
            except ValueError:
                print(f"Invalid data skipped in {file_path}: {line.strip()}")
    return numbers

def compute_mean(data):
    """Computes the mean using basic operations."""
    return sum(data) / len(data) if data else 0

def compute_median(data):
    """Computes the median using basic operations."""
    data.sort()
    length = len(data)
    if length == 0:
        return 0
    if length % 2 == 1:
        return data[length // 2]
    return (data[length // 2 - 1] + data[length // 2]) / 2

def compute_mode(data):
    """Computes the mode using basic operations."""
    if not data:
        return None
    counter = Counter(data)
    max_count = max(counter.values())
    modes = [key for key, value in counter.items() if value == max_count]
    return modes if len(modes) > 1 else modes[0]

def compute_variance(data, mean):
    """Computes the variance using basic operations."""
    if not data:
        return 0
    return sum((x - mean) ** 2 for x in data) / len(data)

def compute_std_dev(variance):
    """Computes the standard deviation using basic operations."""
    return variance ** 0.5

def process_files(file_list):
    """Processes files, transposes results, minimizes local variables."""

    def calculate_statistics(data):
        """Calculates and yields statistics for a single file."""
        yield "Mean", f"{compute_mean(data):.5f}"
        yield "Median", f"{compute_median(data):.5f}"
        yield "Mode", (
    str(compute_mode(data))
    if isinstance(compute_mode(data), list)
    else f"{compute_mode(data):.5f}"
)
        yield "Variance", f"{compute_variance(data, compute_mean(data)):.5f}"
        yield "Std Dev", f"{compute_std_dev(compute_variance(data, compute_mean(data))):.5f}"

    start_time = time.time()
    results = {
        file_name: dict(calculate_statistics(read_file(file_name)))
        for file_name in file_list
        if file_name.endswith(".txt") and os.path.exists(file_name) and read_file(file_name)
    }
    elapsed_time = time.time() - start_time  # Calculate elapsed time directly
    statistics_names = ["Mean", "Median", "Mode", "Variance", "Std Dev"]
    file_names = list(results.keys())
    header = f"{'':<15}" + "".join(f"{file_name:<20}" for file_name in file_names)
    separator = "-" * (15 + len(file_names) * 20)
    output_lines = [header, separator]

    for stat_name in statistics_names:
        line = f"{stat_name:<15} "
        for file_name in file_names:
            line += f"{results[file_name][stat_name]:<20}" #corrected
        output_lines.append(line)

    output_lines.append(separator)
    output_lines.append(f"Execution Time: {elapsed_time:.5f} seconds") # corrected
    final_output = "\n".join(output_lines)

    print(final_output)

    with open("StatisticsResults.txt", "w", encoding='utf-8') as output_file:
        output_file.write(final_output)

def main():
    """Main function to start processing."""
    if len(sys.argv) < 2:
        print("Usage: python compute_statistics.py <file1.txt> <file2.txt> ...")
        sys.exit(1)
    process_files(sys.argv[1:])

if __name__ == "__main__":
    main()
