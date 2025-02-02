"""
convertNumbers.py

Converts numbers, including item numbers, from multiple files.
"""

import sys
import time

def to_binary(number):
    """Converts a positive integer to its binary representation (string)."""
    if number == 0:
        return "0"
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number //= 2
    return binary

def to_hexadecimal(number):
    """Converts a positive integer to its hexadecimal representation (string)."""
    if number == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    while number > 0:
        hexadecimal = hex_chars[number % 16] + hexadecimal
        number //= 16
    return hexadecimal

def convert_numbers(file_paths_arg):
    """Converts numbers, including item numbers, from multiple files."""
    start_time = time.time()
    all_file_results = []
    total_invalid_count = 0

    for file_path in file_paths_arg:
        results = []
        file_invalid_count = 0
        item_number = 1

        try:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                for line in input_file:
                    try:
                        num = int(line.strip())
                        if num < 0:
                            print(f"Invalid data (negative number) in {file_path}: {line.strip()}")
                            file_invalid_count += 1
                            continue
                        binary = to_binary(num)
                        hexadecimal = to_hexadecimal(num)
                        results.append(f"{item_number:<5} {num:<15} {binary:<30} {hexadecimal:<15}")
                        item_number += 1
                    except ValueError:
                        print(f"Invalid data (not an integer) in {file_path}: {line.strip()}")
                        file_invalid_count += 1
                        continue

            if results:
                all_file_results.append(f"Results for file: {file_path}")
                all_file_results.append("-" * 70)
                all_file_results.extend(results)
                all_file_results.append("-" * 70)
                all_file_results.append(f"Invalid Data Count in {file_path}: {file_invalid_count}")
                total_invalid_count += file_invalid_count
                all_file_results.append("")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None, None, None

    end_time = time.time()
    elapsed_time = end_time - start_time

    return all_file_results, total_invalid_count, elapsed_time


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python converter.py file1.txt file2.txt...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    results_data = convert_numbers(file_paths)

    if results_data is not None:
        all_results, total_invalid_data_count, elapsed = results_data

        OUTPUT_TEXT = "" 
        OUTPUT_TEXT += f"{'Item':<5} {'Decimal':<15} {'Binary':<30} {'Hexadecimal':<15}\n"
        OUTPUT_TEXT += "-" * 70 + "\n"
        OUTPUT_TEXT += "\n".join(all_results)
        OUTPUT_TEXT += "\n"
        OUTPUT_TEXT += "-" * 70 + "\n"
        OUTPUT_TEXT += f"Total Invalid Data Count: {total_invalid_data_count}\n"
        OUTPUT_TEXT += f"Elapsed Time: {elapsed:.6f} seconds\n"

        print(OUTPUT_TEXT, end="")

        try:
            with open("ConvertionResults.txt", 'w', encoding='utf-8') as outfile:
                outfile.write(OUTPUT_TEXT)
        except OSError as e:
            print(f"Error writing to file: {e}")

        print("Conversion complete. Results saved to ConvertionResults.txt")
    else:
        print("Conversion process failed due to file errors.")
