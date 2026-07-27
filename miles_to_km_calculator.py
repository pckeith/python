#*************************************************
# Mile to Kilometer Calculator:                  *
# Author:    Keith Caldwell                      *
# Date:      July 27,2026                        *
#*************************************************
# Description:                                   *
# This task is Day 27 of 100 days of Python:     *
# Today we learned a little more about list and  *
# dictionary comprehension, however the biggest  *
# part of the day was starting to work with the  *
# Python tkinter library, and working with the   *
# main Python GUI libraries (no longer limited   *
# to working with Turtle!!)                      *
#                                                *
# On this particular day, I did some "vibe       *
# coding" to get the red, yellow, and green      *
# icons on the heading line: This was beyond my  *
# ability to code from scratch, however nobody   *
# is really coding from scratch anymore, are     *
# they? Most mportant to understand concepts!    *
#                                                *
# Today, not only did we get an overview about   *
# most of the main GUI elements in the tkinter   *
# library, but we also learned about placing the *
# tkinter objects. The 3 ways of placing tkinter *
# GUI objects on Windows are as follows:         *
#                                                *
# Pack -    A non-exact way of "packing" objects *
#           together. Can only specify general   *
#           positional parameters such as "top", *
#           "bottom", "left", and "right".       *
#                                                *
# Place -   Can position a an object at exact x  *
#           and y coordinates within the Window. *
#                                                * 
# Grid -    Imagines your entire program is a    *
#           grid, and you can divide it into any *
#           number of grids you want. Seems to   *
#           be one of the easier options to deal *
#           with, the developer just needs to    *
#           work with relative grids. Let Python *
#           deal with the exact details.         *
#*************************************************

import tkinter as tk
root = tk.Tk()
root.geometry("260x160")  # Accommodate a compact 3x3 layout


def compute_kilometers():
    # Convert the string input to a float
    miles = float(entry.get() or 0) 
    kilometers = miles * 1.60934
    # Rounding to 2 decimal places keeps the GUI clean
    label3.config(text=f"{kilometers:.2f}") 


def validate_int(text):
    # Allow empty string (so users can delete everything) or digits only
    if text == "" or text.isdigit():
        return True
    return False
vcmd = root.register(validate_int)

#********************************************************
# C U S T O M   W I N D O W   T I T L E    A R E A :    *
#********************************************************
# The only purpose of the code in the area below        *
# (until you see the next major area in the program,    *
# identified by a major comment as you see here) was    *
# only to provide a custom window title, with the red,  *
# yellow, and green circles on the left side of the     *
# window title. This required building of a completely  *
# custom frame, and normal window functionality had to  *
# be manually added back in!                            *
#********************************************************

# Hide default OS title bar and borders
root.overrideredirect(True)

# Main window setup (Title bar on top, Content area on bottom)
root.grid_rowconfigure(0, weight=0)  
root.grid_rowconfigure(1, weight=1)  
root.grid_columnconfigure(0, weight=1) 

# --- Window Movement Functions ---
def start_drag(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_drag(event):
    delta_x = event.x - start_x
    delta_y = event.y - start_y
    new_x = root.winfo_x() + delta_x
    new_y = root.winfo_y() + delta_y
    root.geometry(f"+{new_x}+{new_y}")

def close_window(event=None):
    root.destroy()

# Custom Title Bar Frame
title_bar = tk.Frame(root, bg="#e0e0e0", height=30)
title_bar.grid(row=0, column=0, sticky="ew")

title_bar.bind("<Button-1>", start_drag)
title_bar.bind("<B1-Motion>", on_drag)

# Canvas for circles
circle_canvas = tk.Canvas(title_bar, width=65, height=30, bg="#e0e0e0", bd=0, highlightthickness=0)
circle_canvas.pack(side="left", padx=(10, 5))
circle_canvas.bind("<Button-1>", start_drag)
circle_canvas.bind("<B1-Motion>", on_drag)

# Draw circles
red_circle = circle_canvas.create_oval(5,  9, 17, 21, fill="#ff5f56", outline="#e0443e")
circle_canvas.create_oval(25, 9, 37, 21, fill="#ffbd2e", outline="#dea123")
circle_canvas.create_oval(45, 9, 57, 21, fill="#27c93f", outline="#1aab29")

# circle_canvas.tag_bind(red_circle, "<Button-1>", close_window)

# Title text label
title_label = tk.Label(title_bar, text="Miles to Km Converter", bg="#e0e0e0", fg="#333333", font=("Arial", 10, "bold"))
title_label.pack(side="left", pady=5)
title_label.bind("<Button-1>", start_drag)
title_label.bind("<B1-Motion>", on_drag)

# "X" Close Button
close_button = tk.Button(
    title_bar, text="✕", bg="#e0e0e0", fg="#333333", 
    activebackground="#ff5f56", activeforeground="white",
    bd=0, font=("Arial", 11), width=4, height=1, command=close_window
)
close_button.pack(side="right", fill="y")
close_button.bind("<Enter>", lambda e: close_button.config(bg="#d0d0d0"))
close_button.bind("<Leave>", lambda e: close_button.config(bg="#e0e0e0"))



#********************************************************
# S T A N D A R D    W I N D O W    P R O C E S S :     *
#********************************************************
# We're now done with the special processing for the    *
# custom window title. The coding below is to allow     *
# for the main functionality of this program, which is  *
# converting between miles and kilometers, and the GUI  *
# elements on the window supporting this conversion.    *
#********************************************************

# --- 3x3 GRID CONTENT AREA ---
content_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="flat")
content_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)


# --- POPULATING THE 3x3 GRID ---
#Configure row and column weights so the empty cells maintain structure
for i in range(3):
    content_frame.rowconfigure(i, weight=1)
for j in range(3):
    content_frame.columnconfigure(j, weight=1)

entry = tk.Entry(content_frame, width=10, validate="key", validatecommand=(vcmd, '%P'))
entry.grid(row=0, column=1, padx=5, pady=5)
entry.insert(0, 0)

label1 = tk.Label(content_frame,text="Miles",font=("Arial",10,"normal"))
label1.grid(row=0, column=2, padx=5, pady=5)

label2 = tk.Label(content_frame,text="is equal to",font=("Arial",10,"normal"))
label2.grid(row=1, column=0, padx=5, pady=5)

label3 = tk.Label(content_frame,text="0",font=("Arial",10,"normal"))
label3.grid(row=1, column=1, padx=5, pady=5)

label4 = tk.Label(content_frame,text="Km",font=("Arial",10,"normal"))
label4.grid(row=1, column=2, padx=5, pady=5)

button = tk.Button(content_frame,text="Calculate",command=compute_kilometers)
button.grid(row=2, column=1, padx=5, pady=5)


root.mainloop()
