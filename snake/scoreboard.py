from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier",24,"normal")

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.points = 0
        self.hideturtle()
        self.setposition(0,265)
        self.color("white")
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.points}",align=ALIGNMENT,font=FONT)

    def add_one_point(self):
        self.points += 1
        self.clear()
        self.update_scoreboard()

    def game_over(self):
        self.penup()
        self.setposition(0,0)
        self.color("red")
        self.write("GAME OVER",align=ALIGNMENT,font=FONT)


