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
py -3 wordfreq.py (Input txt file) (Generated File Name) --savepath (Generated Folder Name)

Mac
py -3 wordfreq.py (Input txt file) (Generated File Name) --savepath (Generated Folder Name)
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    parser.add_argument("word_freq_file_name")
    parser.add_argument(
        "--savepath",
        dest="output_path",
        help="specify a filepath to save your files"
    )

    parsed_args = parser.parse_args()

    run(
        parsed_args.input_folder,
        parsed_args.word_freq_file_name,
        parsed_args.output_path
    )

def run(input_folder_path, word_list_file, output):

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

        # Sample of 10 words
        print("Word Freq Sample of top 10 words...")
        ten_word_sample = list(word_freq.keys())[:10]
        # for word in ten_word_sample:
            # Word must take up a min of 15 spaces; freq can take min of 8 spaces
            # print("{0:15}{1:8d}".format(word, word_freq[word]))

        # print(f"...")

        sorted_word_freq = order_dict_by_freq(word_freq)
        print(type(sorted_word_freq))
        print(sorted_word_freq)
        # for tuple_freq in sorted_word_freq:
            # count, word = tuple_freq
            # print("{0:15}{1:8d}".format(word, count))

        output = str(output)
        output = output.strip()
        output = os.path.join(r"C:\Users\Austin\PycharmProjects\dictionary", output)
        print(output)
        os.makedirs(output, exist_ok=True)
        print(f"Created directory {output}...")
        with open(os.path.join(output, word_list_file), 'w', encoding='utf-8') as output_file:
            # Generate Word List
            for word in word_list:
                output_file.write(word)
                output_file.write('\n')
            print(f"Created Word Frequency List {word_list_file}...")

        # Generate JSON Word Frequency List
        json_word_freq_file = json_word_freq_list_file + ".json"
        with open(os.path.join(output, json_word_freq_file), 'w', encoding='utf-8') as json_output_file:
            json.dump(sorted_word_freq, json_output_file, ensure_ascii=False, indent=2)



# Convert dict to tuple
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
