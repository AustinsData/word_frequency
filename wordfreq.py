import string
import argparse
import os
import re
import json

"""
Word Freq

This script generates a new file containing a list of words 

Run through command prompt/terminal

Input:
Windows
py -3 wordfreq.py (Input txt file) (Generated File Name) (Generated Folder Name) --savepath (Save Path) 

Mac
python3 wordfreq.py (Input txt file) (Generated File Name) (Generated Folder Name) --savepath (Save Path) 
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    parser.add_argument("word_freq_file_name")
    parser.add_argument("output_folder")
    parser.add_argument(
        "--savepath",
        dest="output_path",
        help="specify a filepath to save your files"
    )

    parsed_args = parser.parse_args()

    run(
        parsed_args.input_folder,
        parsed_args.word_freq_file_name,
        parsed_args.output_folder,
        parsed_args.output_path
    )

def run(input_folder_path, word_list_file, output_folder, output_path):

    filepath = input_folder_path

    word_freq = {}
    word_list = []
    json_word_freq_list_file = word_list_file
    word_list_file = f"{word_list_file}.txt"

    with open(filepath, 'r', encoding='UTF-8') as file:
        # For each line in the file
        for line in file:
            # Remove the punctuation
            line = strip_punct(line)
            line = line.lower()

            # Separate words by spaces into list
            text = line.split()
            print(type(text))

            # Create word list and word freq dict
            print("First Run Initiated...")
            for word in text:
                # word = word.lower()
                if word not in word_freq:
                    word_freq[word] = 0
                    word_list.append(str(word))
                word_freq[word] += 1
            print("First Run Complete...")

            # Delete digits from word list
            for word in word_list:
                if re.search(r"(\d)+", word):
                    print(word)
                    word_list.remove(word)

            # Delete digits again because 1st run did not catch all
            print("Second Run Initiated...")
            for word in word_list:
                if re.search(r"(\d)+", word):
                    print(word)
                    word_list.remove(word)
            print("Second Run Complete...")

            # Sort Word List
            word_list.sort()

        sorted_word_freq = order_dict_by_freq(word_freq)
        print(type(sorted_word_freq))
        print(sorted_word_freq)

        # Reverse dict keys w/ values
        sorted_word_freq_proper = {}
        for key, value in sorted_word_freq.items():
            sorted_word_freq_proper[value] = key

        output_path = str(output_path)
        # output = output.strip()
        # output = os.path.join(r"C:\Users\Austin\PycharmProjects\dictionary", output)
        # print(output)
        file_output_path = os.path.join(output_path, output_folder)
        os.makedirs(file_output_path, exist_ok=True)
        print(f"Created directory {file_output_path}...")
        with open(os.path.join(file_output_path, word_list_file), 'w', encoding='utf-8') as output_file:
            # Generate Word List
            for word in word_list:
                output_file.write(word)
                output_file.write('\n')
            print(f"Created Word Frequency List {word_list_file}...")

        # Generate JSON Word Frequency List
        json_word_freq_file = json_word_freq_list_file + ".json"
        with open(os.path.join(file_output_path, json_word_freq_file), 'w', encoding='utf-8') as json_output_file:
            json.dump(sorted_word_freq_proper, json_output_file, ensure_ascii=False, indent=2)

# Values of Key, then Count
def order_dict_by_freq(dict):
    sorted_val = []
    for key in dict:
        # (dict[key], key) == make a tuple with count, then key
        sorted_val.append((dict[key], key))
    # Since the first val in the tuples are numbers, sorted() will sort based off of that val
    sorted_val = sorted(sorted_val)
    # Sort by largest word freq first
    sorted_val = sorted_val[::-1]
    return sorted_val

def strip_punct(line):
    for char in string.punctuation:
        line = line.replace(char, "")
    return line

if __name__ == "__main__":
    main()
