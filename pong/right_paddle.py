from turtle import Turtle
import time
STARTING_POSITIONS = [(290,20),(290,0),(290,-20)]
TOP_OF_SCREEN = 280
BOTTOM_OF_SCREEN = -230
UP = 90
DOWN = 270


class Right_Paddle:

    def __init__(self):
        
        self.right_paddle = []

        for position in STARTING_POSITIONS:
            self.add_segment(position)
        self.top = self.right_paddle[0]
        self.bottom = self.right_paddle[-1]
    
    def add_segment(self,position):
        new_link = Turtle()
        new_link.shape("square")
        new_link.color("white")
        new_link.penup()
        new_link.goto(position)
        self.right_paddle.append(new_link)
    
    def up(self):
        if self.top.ycor() <= TOP_OF_SCREEN: # Prevent UP after TOP_OF_SCREEN
            self.top.setheading(UP)
            self.move_forward()
            time.sleep(.01)
    
    def down(self):
        if self.bottom.ycor() >= BOTTOM_OF_SCREEN: # Prevent DOWN after BOTTOM_OF_SCREEN
            self.top.setheading(DOWN)
            self.move_forward()
            time.sleep(.01)
     
    def move_forward(self):
        for i in range(len(self.right_paddle) - 1, 0, -1):
            self.right_paddle[i].goto(self.right_paddle[i-1].pos())
        self.top.forward(20)

    def __len__(self):
        return len(self.right_paddle)
    
    def __getitem__(self, index):
        return self.right_paddle[index]