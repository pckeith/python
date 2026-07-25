#*************************************************
# US States Game:                                *
# Author:    Keith Caldwell                      *
# Date:      July 24,2026                        *
#*************************************************
# Description:                                   *
# This task is Day 25 of 100 days of Python:     *
# One of the main reasons I'm learning Python,   *
# is to advance my skills as a Senior Data       *
# Analyst, even to the point of hopefully        *
# beginning to work on Modern Data Engineering   *
# projects, targeting Modern Data Warehouses,    *
# some of which I've already had some exposure   *
# to.                                            *
#                                                *
# The signifigance of Day 25 is, we're finally   *
# starting to move into the areas which will be  *
# useful for Data Analysis and Data Engineering! *
# Today, we're finally starting to work with the *
# Pandas library, something I've been waiting    *
# weeks for! This week we started to work with   *
# some public datasets we used Pandas for (not   *
# super messy or gigantic yet, but you need to   *
# walk before you can run, right?                *
#                                                *
# This game itself is a fairly straightforward   *
# use of the Pandas library, to read and write   *
# to a couple datasets using the DataFrame data  *
# structure for tabular data. This was just the  *
# beginning, Angela says we'll be doing a lot    *
# more complex things with Pandas, NumPy,        *
# Matplotlib and others in the days ahead!!      *
#*************************************************
from turtle import Turtle, Screen
import os
from pathlib import Path
import pandas as pd
from state_input_control import State_Input_Control
from scoreboard import Scoreboard


script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
states_img_filename = "blank_states_img.gif"
states_img_filename_path = str(Path(f"{script_dir}{states_img_filename}"))

screen = Screen()
turtle = Turtle()
screen.title("U.S. States Game")
screen.addshape(states_img_filename_path)
turtle.shape(states_img_filename_path)
state_input_control = State_Input_Control()
screen.tracer(0) 


#***********************************************
# 1. Functions are defined below.              *
#***********************************************
def game_loop(game_on):
    
    answer_state = screen.textinput(title="Guess the State",prompt="Enter another State Name")
    # Sense the Cancel button
    if answer_state is None:
        game_on = False
    # Sense if they clicked OK but didn't type anything
    elif answer_state == "":
        print("User clicked OK but left the input blank.")
    # User typed a valid response
    else:
        state_input_control.try_state_name(answer_state)
        # print(f"User entered: {answer_state}")

    screen.update()
    # time.sleep(.05)

    # Repeatedly call game_loop every 100ms if game is on
    if game_on:
        screen.ontimer(lambda: game_loop(game_on), 100)
    else:
        exit_game()

def exit_game():
    screen.bye()


#***********************************************
# 2. Main body of the program is below.        *
#***********************************************
game_on = True

game_loop(game_on)

# CRITICAL: This keeps the window open and processing events
screen.mainloop()