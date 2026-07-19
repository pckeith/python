import turtle
import time

class Ball(turtle.Turtle):

    # Speed variables (Deltas)
    dx = 3  
    dy = 2

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.is_moving = True

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_off_side(self):
        self.dx *= -1

    def bounce_off_top_bottom(self):
        self.dy *= -1

