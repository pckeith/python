from turtle import Turtle
import pandas as pd
import os
from pathlib import Path
from scoreboard import Scoreboard
scoreboard = Scoreboard()
turtle = Turtle(visible=False)

class State_Input_Control:

    def __init__(self):
        turtle.hideturtle()
        turtle.penup()
        self.remaining_states = pd.DataFrame()
        self.correctly_guessed = pd.DataFrame()

        script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
        states_filename = "50_states.csv"
        self.states_file_path = Path(f"{script_dir}{states_filename}")
        self.remaining_states = pd.read_csv(self.states_file_path).dropna()
        self.remaining_states.state = self.remaining_states.state.str.lower()
        nbr_states_remaining = len(self.remaining_states)
        scoreboard.refresh_states_remaining(nbr_states_remaining)
        scoreboard.update_scoreboard()

    def try_state_name(self, guess):
        guess = guess.lower()    
        #self.remaining_states[self.remaining_states.state == guess]

        if guess in self.remaining_states.state.values:
            self.add_state_name(guess)
        else:
            print(f"{guess} not one of remaining states")

    def add_state_name(self, guess):
        # Add the item to the map
        state_info = self.remaining_states[self.remaining_states.state.values == guess]
        x_coord = int(state_info.x.values[0])
        y_coord = int(state_info.y.values[0])
        turtle.goto(x_coord,y_coord)
        turtle.write(state_info.state.values[0])

        # Lookup and safely move the item
        if guess in self.remaining_states.state.values:
            self.correctly_guessed = pd.concat([self.correctly_guessed, state_info], ignore_index=True)
            self.remaining_states = self.remaining_states[self.remaining_states.state != guess]
            nbr_states_remaining = len(self.remaining_states)
            scoreboard.add_one_point()
            scoreboard.refresh_states_remaining(nbr_states_remaining)
            print(f"remaining states to be named= {nbr_states_remaining}")
