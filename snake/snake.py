from turtle import Turtle
STARTING_POSITIONS = [(0,0),(-20,0),(-40,0)]
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:

    def __init__(self):
        
        self.snake = []

        for position in STARTING_POSITIONS:
            self.add_segment(position)
        self.head = self.snake[0]
    
    def add_segment(self,position):
        new_link = Turtle()
        new_link.shape("square")
        new_link.color("white")
        new_link.penup()
        new_link.goto(position)
        self.snake.append(new_link)

    def extend(self):
        self.add_segment(self.snake[-1].position())
    
    def up(self):
        if self.head.heading() != DOWN: # Prevent suicide U turn
            self.head.setheading(UP)
        
    def down(self):
        if self.head.heading() != UP: # Prevent suicide U turn
            self.head.setheading(DOWN)
    
    def left(self):
        if self.head.heading() != RIGHT: # Prevent suicide U turn
            self.head.setheading(LEFT)
        
    def right(self):
        if self.head.heading() != LEFT: # Prevent suicide U turn
            self.head.setheading(RIGHT)

    def move_forward(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].goto(self.snake[i-1].pos())
        self.head.forward(20)

    def __len__(self):
        return len(self.snake)
    
    def __getitem__(self, index):
        return self.snake[index]
