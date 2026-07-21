from turtle import Turtle

STARTING_POSITION = (0, -280)
ORIENTATION = 90
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("black")
        self.shape("turtle")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(ORIENTATION)
        self.showturtle()

    def move_forward(self):
        self.forward(MOVE_DISTANCE)
    
    def move_backward(self):
        if self.ycor() > -250:
            self.backward(MOVE_DISTANCE)

    def goto_start_position(self):
        self.goto(STARTING_POSITION)