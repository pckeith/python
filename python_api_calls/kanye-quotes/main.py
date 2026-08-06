#*****************************************************
# Kanye Quotes:                                      *
# Author:    Keith Caldwell                          *
# Date:      August 5,2026                           *
#*****************************************************
# Description:                                       *
# This task is Day 33 of 100 days of Python:         *
# This was one of 2 API tasks to build today, this   *
# was super simple: Just call the Kanye API, which   *
# does nothing more than return a Kanye quote. Once  *
# the quote is received, just populate it into the   *
# quote box. Pretty simple, however would be a nice  *
# intro to APIs, for someone who has never done an   *
# API before.                                        *
#*****************************************************
from pathlib import *
import os
import requests
import json
from tkinter import *


def get_quote():
    response = requests.get(url="https://api.kanye.rest/")
    response.raise_for_status()  # Raise an error for any response other than 200!
    response_text = response.text
    data_dict = json.loads(response_text)
    kanye_quote = data_dict["quote"]
    canvas.itemconfig(quote_text, text=kanye_quote)
    # print(kanye_quote)


window = Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=50)

script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
background_file = "background.png"
background_path = str(Path(script_dir) / background_file)
kanye_file = "kanye.png"
kanye_path = str(Path(script_dir) / kanye_file)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file=background_path)
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(150, 207, text="Kanye Quote Goes HERE", width=250, font=("Arial", 30, "bold"), fill="white")
canvas.grid(row=0, column=0)

kanye_img = PhotoImage(file=kanye_path)
kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(row=1, column=0)

get_quote()

window.mainloop()