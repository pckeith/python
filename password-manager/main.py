#*************************************************
# Password Manager:                              *
# Author:    Keith Caldwell                      *
# Date:      July 29,2026                        *
#*************************************************
# Description:                                   *
# This task is Day 29 of 100 days of Python:     *
# Today we continued to learn more about the     *
# Python tkinter library, and how to make even   *
# more professional looking windows apps. The    *
# app we're building today is a password         *
# manager.                                       *
#                                                *
# Similar to the professional password managers  *
# managers commonly available commercially, the  *
# the password manager I'm building today will   *
# will allow building of passwords much like     *
# other modern password managers. However, this  *
# password manager will store results on your    *
# computer (instead of a centralized database).  *
#                                                *
# There are some who will argue this may         *
# actually be more safe than a remote 3rd party  *
# vault (such as LastPass, etc.). These          *
# commercial products would certainly be         *
# expected to employ many security features,     *
# however would also be a well-known and         *
# constant target for many skilled hackers.      *
#*************************************************
from tkinter import *
from pathlib import *
import os
import random
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
WHITE = "white"
FONT_NAME = "Ariel"
BOLD = "bold"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    '''
        Generate a new password in the following format:
            Begins with unique uppercase character
            14 characters, including uppercase / lowercase, and numbers
            ends with a symbol 
    '''  
    
    unique_uppercase = ["A", "C", "D", "E", "F", "G", "H", "J", 
        "K", "M", "N", "P", "Q", "R", "T", "V", "W", "X", "Y"]
    unique_lowercase_letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "j", "k", 
        "m", "n", "p", "q", "r", "s", "t", "u", "v", "w", 
        "x", "y", "z", "3", "4", "6", "7", "8", "9"]
    unique_numbers = ["3", "4", "6", "7", "8", "9"]
    password_symbols = ["!", "#", "$", "%", "&", "*", "+", "-", 
        "?", "@", "^", "_"]

    # Generate the pieces
    start_char = random.sample(unique_uppercase, k=1)
    combined_list = random.sample(unique_uppercase, k=8) + random.sample(unique_lowercase_letters, k=4) + random.sample(unique_numbers, k=2)
    middle_chars = random.sample(combined_list, k=14)
    end_char = random.sample(password_symbols, k=1)

    # Combine lists and convert to a single string
    final_password = "".join(start_char + middle_chars + end_char)

    # Clear entry3 and insert the new password string
    entry3.delete(0, END)
    entry3.insert(0, final_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    # Add the password to the file

    script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
    pwlist_filename = "userdata.txt"
    pwlist_filename_path = str(Path(f"{script_dir}{pwlist_filename}"))

    website = entry1.get()
    id = entry2.get()
    pw = entry3.get()
    newpw_line_to_write = f"{website}  |  {id}  |  {pw}\n"

    # Open file for appending (creates file if missing)
    with open(pwlist_filename_path, "a") as file:
        file.write(newpw_line_to_write)

    entry1.delete(0, END)
    entry1.insert(0,"")
    entry2.delete(0, END)
    entry2.insert(0,"your_email@your_company.com")
    entry3.delete(0, END)
    entry3.insert(0,"")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20,bg=WHITE)
frame = Frame(window,padx=20,pady=20,bg=WHITE)
frame.grid(row=5, column=3)

script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
pwlock_img_filename = "logo.png"
pwlock_img_filename_path = str(Path(f"{script_dir}{pwlock_img_filename}"))
pwlock_img = PhotoImage(file=pwlock_img_filename_path)

canvas = Canvas(width=200,height=200,bg=WHITE,highlightthickness=0)
# Image is half of the canvas
canvas.create_image(100,100,image=pwlock_img)
canvas.grid(row=0, column=1, sticky="ew")

#******************************
# First Row Elements          * 
# (directly below lock icon)  *
#******************************
label1 = Label(window,text="Website: ",bg=WHITE,font=(FONT_NAME,10,"normal"))
label1.grid(row=1, column=0)

entry1 = Entry(window, relief="solid", width=35)
entry1.grid(row=1, column=1, columnspan=2, sticky="ew")
entry1.insert(0,"")
entry1.focus()  # Set focus on the website entry, put cursor here!

#******************************
# Second Row Elements         *
#******************************
label2 = Label(window,text="Email / Username: ",bg=WHITE,font=(FONT_NAME,10,"normal"))
label2.grid(row=2, column=0)

entry2 = Entry(window, relief="solid", width=35)
entry2.grid(row=2, column=1, columnspan=2, sticky="ew")
entry2.insert(0,"keith.caldwell@masterdataconnect.com")

#******************************
# Third Row Elements          *
#******************************
label3 = Label(window,text="Password: ",bg=WHITE,font=(FONT_NAME,10,"normal"))
label3.grid(row=3, column=0)

entry3 = Entry(window, relief="solid", width=21)
entry3.grid(row=3, column=1, sticky="ew")
entry3.insert(0,"")

button1 = Button(window,text="Generate Password",command=generate_password)
button1.grid(row=3, column=2)

#******************************
# Fourth Row Elements         *
#******************************
button2 = Button(window,width=36,text="Add",command=add_password)
button2.grid(row=4, column=1, columnspan=2, sticky="ew")


# Automatically add padding to all widgets inside the window
for widget in window.winfo_children():
    # Skip the canvas if you don't want extra padding around the logo
    if not isinstance(widget, Canvas):
        widget.grid_configure(padx=5, pady=5)


window.mainloop()