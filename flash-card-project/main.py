#****************************************************************
# Flash Card Project:                                           *
# Author:    Keith Caldwell                                     *
# Date:      August 1, 2026                                     *
#****************************************************************
# Description:                                                  *
# This task is for Day 31 of 100 days of Python:                *
#                                                               *
# Today's project is a Flash card project, which helps users    * 
# remember the meaning of a set of words. Each will be          *
# individually presented to the user, in Flash Card format.     *
#                                                               *
# When a word shows up on a Flash Card, the user has 3 seconds  *
# to correctly identify it. If the word cannot be correctly     *
# identified (before the answer is automatically provided from  *
# the back of the card), it stays in the deck. Any cards        *
# remaining in the deck will keep on showing up, until the      *
# user correctly identifies the meaning.                        *
#                                                               *
# The user communicates success or failure, by clicking on      *
# either a green check mark (to indicate success), or a red     *
# X (to indicate failure).                                      *
#                                                               *
# The words displayed on the flash cards have been sourced      *
# from a website called Wiktionary, at the following URL:       *
#                                                               *
# https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists     *
#                                                               *
# Within the above-mentioned URL, there are separate URLs       *
# containing word frequency lists for many different languages. *
# In the default project for Python 100 class, the instructor   *
# (Angela Yu) had already exported and curated a list of the    *
# top 1000 French words. However, in my case I wanted the       *
# Flash Cards to be for Brazilian Portuguese, therefore I       *
# developed my own top 1000 Portuguese words list, using the    *
# steps shown below:                                            *
#                                                               *
# 1) Download however many words you want from the              *
#    language-specific list from the URL above (i.e.: I         *
#    selected Brazilian Portuguese). You'll get markup with     *
#    the actual words in the middle.                            *
# 2) Parse out the specific words from the markup language in   *
#    each cell.                                                 *
# 3) Open a Google spreadsheets document, and paste the words   *
#    from your Excel document, into your Google document.       *
# 4) On the first cell in the B column (to the right of the A   *
#    column where you pasted the untranslated words), paste     *
#    this formula =GOOGLETRANSLATE(A1,"pt","en"), which means   *
#    in my case, translating from Portuguese to English. Use    *
#    the correct source language code for your source language. *
# 5) Copy the B1 column all the way down, just like you'd do to *
#    repeat a formula on Excel.                                 *
# 6) Copy the translated column back to your Excel worksheet.   *
#****************************************************************
from tkinter import messagebox
from tkinter import *
from pathlib import *
import os
import random
import json
from PIL import Image, ImageTk
import time

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- FUNCTION DEFINITIONS-------------------- #
def load_input_word_list():
    # Use global variables to update the existing elements on the canvas
    global source_card_word1, source_card_word2

    script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
    input_words_to_learn_file = "input_words_to_learn.json"
    input_words_to_learn_path = str(Path(script_dir) / "data" / input_words_to_learn_file)

    output_words_learned_file = "output_words_learned.json"
    output_words_learned_path = str(Path(script_dir) / "data" / output_words_learned_file)

    # Check if file exists and is not empty
    if os.path.exists(output_words_learned_path) and os.path.getsize(output_words_learned_path) > 0:
        with open(output_words_learned_path, "r", encoding="utf-8") as file:
            words_learned = json.load(file)

    
    # This JSON input file is created by a one-time program (onetime_create_json_words_input.py)
    try:
        with open(input_words_to_learn_path, "r", encoding="utf-8") as file:
            words_to_learn = json.load(file)
    except FileNotFoundError:
        canvas.itemconfig(source_card_word1, text=f"filepath {input_words_to_learn_path}", font=("Helvetica", 10, "italic"))
        canvas.itemconfig(source_card_word2, text="Not found!!", fill="red")
        return
    else:
        return words_to_learn


def get_weighted_random_word(words_to_learn):
    """
    Selects a single word dictionary from the list, weighted by its 'Frequency' value.
    """
    # 1. Extract the frequency values to use as weights
    weights = [word["Frequency"] for word in words_to_learn]
    
    # 2. Use random.choices to pick a word based on those weights
    # random.choices returns a list, so we grab the first element [0]
    selected_word_dict = random.choices(words_to_learn, weights=weights, k=1)[0]
    
    return selected_word_dict

def get_next_card():

    global selected_row

    canvas.itemconfig(canvas_image, image=cardfront_img)
    # Get your new word from the dictionary/list
    selected_row = get_weighted_random_word(words_to_learn)

    key_iterator = iter(selected_row)
    subject_key = next(key_iterator)
    new_word = selected_row[subject_key]
    canvas.itemconfig(source_card_word1, text=subject_key, fill="black")
    canvas.itemconfig(source_card_word2, text=new_word, fill="black")

    # Extract remaining data needed for the flip
    translate_key = next(key_iterator)
    translated_word = selected_row[translate_key]
    
    # Schedule the flip to happen in 3000 milliseconds (3 seconds)
    canvas.after(3000, flip_card, translate_key, translated_word)  


def flip_card(translate_key, translated_word):
    canvas.itemconfig(canvas_image, image=cardback_img)
    canvas.itemconfig(source_card_word1, text=translate_key, fill="white")
    canvas.itemconfig(source_card_word2, text=translated_word, fill="white")


def handle_right_button():

    # Use global variables to bring in words_learned dictionary
    global words_learned

    # First, add the current word to the list of words learned 
    words_learned.append(selected_row)
    script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
    output_words_learned_file = "output_words_learned.json"
    output_words_learned_path = str(Path(script_dir) / "data" / output_words_learned_file)
    with open(output_words_learned_path, "w", encoding="utf-8") as json_file:
        json.dump(words_learned, json_file, indent=4, ensure_ascii=False)

    # Second, remove the current word from the list of words to be learned
    new_word = selected_row[subject_key]
    remove_word = new_word
    # Filter rows using list comprehension combined with dictionary comprehension
    # It keeps the row as long as the subject key doesn't match the remove word
    filtered_data = [
        {key: value for key, value in row.items()} 
        for row in words_to_learn 
        if row.get(subject_key) != remove_word
    ]
    script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
    input_words_to_learn_file = "input_words_to_learn.json"
    input_words_to_learn_path = str(Path(script_dir) / "data" / input_words_to_learn_file)
    with open(input_words_to_learn_path, "w", encoding="utf-8") as json_file:
        json.dump(filtered_data, json_file, indent=4)


    # Finally, get the next card 
    get_next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card Project")
window.config(padx=20,pady=20,bg=BACKGROUND_COLOR)
frame = Frame(window,padx=20,pady=20,bg=BACKGROUND_COLOR)
frame.grid(row=2, column=2)

script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
cardfront_img_filename = "card_front.png"
cardfront_img_filename_path = str(Path(script_dir) / "images" / cardfront_img_filename)
cardfront_img = PhotoImage(file=cardfront_img_filename_path)

cardback_img_filename = "card_back.png"
cardback_img_filename_path = str(Path(script_dir) / "images" / cardback_img_filename)
cardback_img = PhotoImage(file=cardback_img_filename_path)

# --- PILLOW RESIZING LOGIC ---
pil_img = Image.open(cardfront_img_filename_path)
pil_img_resized = pil_img.resize((700, 500), Image.Resampling.LANCZOS)
cardfront_img = ImageTk.PhotoImage(pil_img_resized)

pil_img = Image.open(cardback_img_filename_path)
pil_img_resized = pil_img.resize((700, 500), Image.Resampling.LANCZOS)
cardback_img = ImageTk.PhotoImage(pil_img_resized)

canvas = Canvas(width=700,height=500,bg=BACKGROUND_COLOR,highlightthickness=0)
# Image is half of the canvas
canvas_image = canvas.create_image(350,250,image=cardfront_img)

x_center = 350  # Horizontal canvas position for center of word
y_top_word = 150 # Vertical canvas position for top of word
source_card_word1 = canvas.create_text(
    x_center, y_top_word, text="Title", fill="black", font=("Helvetica", 24,"italic"), anchor="center"
)
x_center = 350  # Horizontal canvas position for center of word
y_top_word = 250 # Vertical canvas position for top of word
source_card_word2 = canvas.create_text(
    x_center, y_top_word, text="word", fill="black", font=("Helvetica", 36, "bold"), anchor="center"
)

canvas.grid(row=0, column=0, columnspan=2,sticky="nsew")

#******************************
# First Row Elements          * 
# (buttons below display)     *
#******************************
wrong_img_filename = "wrong.png"
wrong_img_filename_path = str(Path(script_dir) / "images" / wrong_img_filename)
wrong_img = PhotoImage(file=wrong_img_filename_path)
button_wrong = Button(window,image=wrong_img,command=get_next_card)
button_wrong.grid(row=1, column=0)

right_img_filename = "right.png"
right_img_filename_path = str(Path(script_dir) / "images" / right_img_filename)
right_img = PhotoImage(file=right_img_filename_path)
button_right = Button(window,image=right_img,command=handle_right_button)
button_right.grid(row=1, column=1)


# Automatically add padding to all widgets inside the window
for widget in window.winfo_children():
    # Skip the canvas if you don't want extra padding around the logo
    if not isinstance(widget, Canvas):
        widget.grid_configure(padx=5, pady=5)


# Get the list of remaining words left to learn
words_to_learn = load_input_word_list()
words_learned = []
selected_row = []

# Populate subject, and the first word left to learn
inner_dict = words_to_learn[1]
key_iterator = iter(inner_dict)
subject_key = next(key_iterator)
translate_key = next(key_iterator)

get_next_card()

window.mainloop()

