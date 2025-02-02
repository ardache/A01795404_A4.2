"""
word_count.py

Counts distinct words and their frequencies from a list of files,
including total word count and sorted output (most frequent first).
"""

import sys
import time

def count_words(file_paths_arg):
    """Counts distinct words and their frequencies from multiple files."""
    start_time = time.time()
    word_counts_dict = {}  # Changed name to avoid shadowing
    file_errors_list = [] # Changed name to avoid shadowing

    for file_path in file_paths_arg:
        try:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                for line in input_file:
                    words = line.split()
                    for a_word in words: # Changed name to avoid shadowing
                        cleaned_word = a_word.strip(".,!?;:\"'").lower()
                        if cleaned_word:
                            word_counts_dict[cleaned_word] = word_counts_dict.get(cleaned_word, 0) + 1
        except FileNotFoundError:
            file_errors_list.append(file_path)
            print(f"Error: File '{file_path}' not found.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    return word_counts_dict, file_errors_list, elapsed_time


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python word_count.py file1.txt file2.txt...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    word_count_data = count_words(file_paths)

    if word_count_data:
        word_counts, file_errors, elapsed = word_count_data

        output_text = "" #Changed name to snake_case
        output_text += f"{'Word':<20} {'Frequency':<10}\n"
        output_text += "-" * 30 + "\n"

        # Sort by frequency (second element of the tuple) in descending order
        sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

        for word, count in sorted_word_counts:
            output_text += f"{word:<20} {count:<10}\n"

        output_text += "-" * 30 + "\n"

        total_words = sum(word_counts.values())
        output_text += f"Total words processed: {total_words}\n"

        output_text += f"Elapsed Time: {elapsed:.6f} seconds\n"

        if file_errors:
            output_text += f"File Errors: {', '.join(file_errors)}\n"

        print(output_text, end="")

        try:
            with open("WordCountResults.txt", 'w', encoding='utf-8') as outfile:
                outfile.write(output_text)
        except OSError as e:
            print(f"Error writing to file: {e}")

        print("Word count complete. Results saved to WordCountResults.txt")
    else:
        print("Word count process failed due to file errors.")