#*************************************************
# Nato Alphabet Translator:                      *
# Author:    Keith Caldwell                      *
# Date:      July 25,2026                        *
#*************************************************
# Description:                                   *
# This task is Day 26 of 100 days of Python:     *
# Today we learned about Python List and         *
# Dictionary comprehension. This task we're      *
# doing today seems like a fairly elementary     *
# use of Pandas (as I'm writing this             *
# description), however let's see how easy it    *
# is once I get into writing the code!           *
#                                                *
# This Python script will read in a CSV file     *
# (nato_phonetic_alphabet.csv), which is a       *
# translation between each letter of the         *
# alphabet, and the NATO code words translating  *
# between an alphabet character and the NATO     *
#  keyword. For example: A,B,C,D,E =             *
# "Alpha","Bravo", "Charlie", "Delta", "Echo"    *
# Although I just listed the first 5 above,      *
# there actually is one NATO translation word    *
# for each letter of the English alphabet.       *
#                                                *
# This script will allow the user to enter in a  *
# word, and for each word the user enters, the   *
# program will output a Python list of the NATO  *
# keywords corresponding to each letter of the   *
# word input (converting each letter of the      *
# word, to the corresponding NATO translation    *
# word).                                         *
#*************************************************
import os
from pathlib import Path
import pandas as pd
from art import logo

script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
nato_phonetic_filename = "nato_phonetic_alphabet.csv"
nato_phonetic_filepath = str(Path(f"{script_dir}{nato_phonetic_filename}"))
continue_conversion = True

#********************************************************************
# Convert the NATO Phonetics into a dataframe, which has both a     *
# letter and a NATO translation code on each row. The proper way    *
# to do this, is to use the iterrows function, which allows the     *
# attributes to be handled as individual values instead of series.  *
#********************************************************************
df_nato = pd.read_csv(nato_phonetic_filepath)
nato_dict = {row.letter: row.code for (index, row) in df_nato.iterrows()}


while continue_conversion:

    #***************************************
    # Print the logo, and then input the   *
    # word, in the line below              *
    #***************************************
    print("\n"*155)
    print(logo)
    word = input("What word do you want to translate? ").upper()

    #***************************************
    # Print out the NATO translation       *
    #***************************************
    nato_translation = [nato_dict[letter] for letter in word if letter in nato_dict]
    print(nato_translation)
    print ("\n\n")

    while True:
        another_word = input("Translate another word (Y or N)? ").upper()
        if (another_word == "Y") or (another_word == "N"):
            if another_word == "N":
                continue_conversion = False
            break


