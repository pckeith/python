#****************************************************************
# Flash Card Project:                                           *
# Author:    Keith Caldwell                                     *
# Date:      August 2, 2026                                     *
#****************************************************************
# Description:                                                  *
# This is a one-time program, to re-configure the input words   *
# csv file into the JSON file format, and re-write as           *
# file name: input_words_to_learn.json.                         *
#                                                               *
# The main program will read words from the "to learn" json     *
# file, and then (over time) re-write to the "learned" json     *
# file, which is referenced in the main Python routine for      *
# this project.                                                 *
#                                                               *
#****************************************************************
import csv
import json
from pathlib import *
import os

def csv_to_json(csv_file_path, json_file_path):
    # Using 'utf-8-sig' automatically removes the '\ufeff' BOM marker
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # data = [row for row in csv_reader]
        data = []
        for row in csv_reader:
            row['Frequency'] = int(row['Frequency'])
            data.append(row)
        
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        # ensure_ascii=False keeps characters like 'ã' and 'ê' in readable form
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# Define your file paths here
script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
input_words_csv = "portuguese_words.csv"
input_words_csv_path = str(Path(script_dir) / "data" / input_words_csv)
input_words_to_learn_json = "input_words_to_learn.json"
input_words_to_learn_json_path = str(Path(script_dir) / "data" / input_words_to_learn_json)

csv_file_path = input_words_csv_path
json_file_path = input_words_to_learn_json_path

# Execute the function
csv_to_json(csv_file_path, json_file_path)
print(f"Successfully converted '{csv_file_path}' to '{json_file_path}'!")