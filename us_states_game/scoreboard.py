from turtle import Turtle
import os
from pathlib import Path

ALIGNMENT = "center"
FONT = ("Courier",15,"normal")
SCREEN_TOP_SCORE_START = (-120, 260)
SCREEN_TOP_HISCORE_START = (120, 260)
SCREEN_BOTTOM_STATES_REM_START = (-10, -290)

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
        high_score_filename= "high_score.txt"
        self.high_score_file_path = Path(f"{script_dir}{high_score_filename}")
        self.points = 0
        self.high_score = 0
        self.nbr_states_remaining = 0
        self.penup()
        self.hideturtle()
        self.setposition(0,265)
        self.color("black")
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.update_high_score()
        self.goto(SCREEN_TOP_SCORE_START)
        self.write(f"Your score: {self.points}",align=ALIGNMENT,font=FONT)
        self.goto(SCREEN_TOP_HISCORE_START)
        self.write(f"Hi Score: {self.high_score}",align=ALIGNMENT,font=FONT)
        self.goto(SCREEN_BOTTOM_STATES_REM_START)
        self.write(f"States Remaining to name: {self.nbr_states_remaining}",align=ALIGNMENT,font=FONT)
    
    
    def update_high_score (self):
        self.penup()
        if self.high_score == 0:
            file_path = self.high_score_file_path 
            if file_path.is_file():
                with open(file_path, "r") as file:
                    first_line = file.readline().strip()
                    if first_line.startswith("high_score="):
                        # Extract everything after the '=' sign
                        score_str = first_line.split("=")[1]
                        self.high_score = int(score_str)
                    else:
                        self.high_score = 0
            else:
                with open(file_path, "w") as file:
                    file.write(f"high_score={0}")

        if self.points > self.high_score:
            self.high_score = self.points
            file_path = self.high_score_file_path
            with open(file_path, "w") as file:
                file.write(f"high_score={self.high_score}")


    def add_one_point(self):
        self.points += 1
        self.update_scoreboard()

    def refresh_states_remaining(self,nbr_states_remaining):
        self.nbr_states_remaining = nbr_states_remaining
        self.update_scoreboard()


    def game_over(self):
        self.penup()
        self.setposition(0,0)
        self.color("red")
        self.write("GAME OVER",align=ALIGNMENT,font=FONT)


