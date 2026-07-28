#*************************************************
# Pomodoro Timer:                                *
# Author:    Keith Caldwell                      *
# Date:      July 28,2026                        *
#*************************************************
# Description:                                   *
# This task is Day 28 of 100 days of Python:     *
# Today we learned more about the python         *
# tkinter library, and how to make eve more      *
# professional looking windows apps. The app I   *
# built today is fairly simple (I'll explain     *
# details below), however when I finished the    *
# app today I was impressed how nice it looked,  *
# and I think may find it useful in everyday     *
#  life.                                         *
#                                                *
# The Python app I built today, is called a      *
# Pomodoro timer. The Pomodoro Technique is a    *
# time management method that uses a timer to    *
# break work into 25-minute focus intervals      *
# separated by short breaks. Created by          *
# Francesco Cirillo in the late 1980s, it's      *
# named after the Italian word for tomato,       *
#  because he used a tomato-shaped kitchen       *
#  timer.                                        *
#                                                *
# How It Works:                                  *
# Pick a task from your to-do list.              *
# Set a timer for 25 minutes.                    *
# Work on the task with no distractions until    *
# the timer rings.                               *
# Take a 5-minute break to stretch or rest.      *
# Repeat this cycle 4 times.                     *
#                                                *
# This script is a visual timer, with just four  *
# elements:                                      *
# 1) A timer showing on a tomato image           *
# 2) A start button.                             *
# 3) A reset button.                             *
# 4) A label at bottom, which adds a checkmark   *
#    for each Pomodor sequence you complete.     *
#                                                *
# Just hit the Start button, and the 25 minute   *
# timer will begin. After 25 minutes, it will    *
# indicate a 5 minute break (and add a           *
# checkmark, indicating you've completed a       *
# Pomodoro (will also send a chime, and  put     *
# the screen on top).                            *
#                                                *
# See how many Pomodorow sequences you can       *
# complete! Hit the Reset button at any time     *
# to reset the count and start over. Hit X on    *
# top right of window to quit.                   *
#*************************************************
import winsound
from tkinter import *
from pathlib import *
import os
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
TIMER = "Timer"
BREAK = "Break"
CHECK_MARK = "✓"
WORK_MIN = .5
SHORT_BREAK_MIN = .1


# Global variables
timer_id = None
pomodoro_count = 0
current_phase = "work" # Tracks whether we are in "work" or "break" phase

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    """Resets the timer, labels, counters, and clears scheduled countdowns."""
    global timer_id, pomodoro_count, current_phase
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    
    pomodoro_count = 0
    current_phase = "work"
    
    canvas.itemconfig(timer_text, text="00:00", fill="white")
    label1.config(text=TIMER, fg=GREEN)
    label2.config(text="")

    # Re-enable the start button on reset
    start_button.config(state="normal")


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def update_timer(seconds_left):
    """Calculates the time formatting and schedules the next second tick."""
    global timer_id, pomodoro_count, current_phase
    
    mins, secs = divmod(seconds_left, 60)
    time_string = f"{mins:02d}:{secs:02d}"

    canvas.itemconfig(timer_text, text=time_string)

    if seconds_left > 0:
        # 2. Save the loop identifier to the global variable
        timer_id = window.after(1000, update_timer, seconds_left - 1)
    else:
        timer_id = None
        if current_phase == "work":
            # Work finished -> Start Break
            current_phase = "break"
            pomodoro_count += 1
            repeated_checks = CHECK_MARK * pomodoro_count
            
            label1.config(text=BREAK, fg=PINK)
            label2.config(text=repeated_checks)
            canvas.itemconfig(timer_text, fill="red")

            # Plays the Windows Information chime
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            
            # Forces the window to the top of all open screens
            window.attributes("-topmost", True)
            window.attributes("-topmost", False) # Reset so it does not stay permanently stuck on top
            
            # Automatically start the 5-minute break countdown
            start_countdown(SHORT_BREAK_MIN)
        else:
            # Break finished -> Start Work again
            current_phase = "work"
            label1.config(text=TIMER, fg=GREEN)
            canvas.itemconfig(timer_text, fill="white")
            
            # Automatically restart the 20-minute work countdown
            start_countdown(WORK_MIN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def start_countdown(minutes):
    """Initializes and triggers the countdown process if not already running."""
    global timer_id
    
    # 1. Check if the timer is already running. If yes, ignore the click.
    if timer_id is not None:
        return 

    # Disable the start button so it cannot be clicked while running
    start_button.config(state="disabled")

    total_seconds = int(minutes * 60)
    update_timer(total_seconds)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50,pady=50,bg=YELLOW)
frame = Frame(window, bg=YELLOW)
frame.grid(row=5, column=3)

script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
tomato_img_filename = "tomato.png"
tomato_img_filename_path = str(Path(f"{script_dir}{tomato_img_filename}"))
tomato_img = PhotoImage(file=tomato_img_filename_path)


label1 = Label(window,text=TIMER,bg=YELLOW,fg=GREEN,font=(FONT_NAME,30,"normal"))
label1.grid(row=0, column=1)

canvas = Canvas(width=250,height=300,bg=YELLOW,highlightthickness=0)
# Image is half of the canvas
canvas.create_image(125,150,image=tomato_img)
timer_text = canvas.create_text(125,170,text="00:00",fill="white",font=(FONT_NAME,25,"bold"))
canvas.grid(row=1, column=1)

start_button = Button(window, text="Start", command=lambda: start_countdown(WORK_MIN))
start_button.grid(row=2, column=0)

reset_button = Button(window, text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)

label2 = Label(window,text="",bg=YELLOW,fg=GREEN,font=(FONT_NAME,30,"bold"))
label2.grid(row=3, column=1)


window.mainloop()