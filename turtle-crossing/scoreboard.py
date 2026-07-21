from turtle import Turtle
FONT = ("Courier", 24, "normal")

SCREEN_LEVEL_WORD_START = (-20, 260)
SCREEN_LEVEL_NBR_START = (50, 260)
GAME_OVER_MSG_START = (-10,0)


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.level = 1
        self.successfully_crossed_street = False
        self.game_is_on = True
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears the screen and draws the updated scores."""
        self.clear()

        # Player level
        self.goto(SCREEN_LEVEL_WORD_START )
        self.write("LEVEL:", align="center", font=("Courier", 20, "normal"))
        self.goto(SCREEN_LEVEL_NBR_START)
        self.write(self.level, align="center", font=("Courier", 20, "normal"))

        if self.game_is_on == False:
            pass

        if not self.game_is_on:
            self.goto(GAME_OVER_MSG_START)
            self.color("red")
            self.write("GAME OVER", align="center", font=("Courier", 20, "bold"))


    def next_level(self):
        """Increments the player level, and refreshes display."""
        self.level += 1
        self.update_scoreboard()
