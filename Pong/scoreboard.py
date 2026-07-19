import turtle
SCREEN_SERVE_MSG_START = (-10,0)
SCREEN_BOTTOM_MIDDLE = (0,-290)
SCREEN_BOTTOM_MSG_START = (-6,-280)

class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.print_type_s_to_serve = False
        self.update_scoreboard()


    def update_scoreboard(self):
        """Clears the screen and draws the updated scores."""
        self.clear()
        # Left player score
        self.goto(-100, 200)
        self.write(self.left_score, align="center", font=("Courier", 80, "normal"))
        # Right player score
        self.goto(100, 200)
        self.write(self.right_score, align="center", font=("Courier", 80, "normal"))
        # Type q or Q to quit (on bottom of screen)

        if self.print_type_s_to_serve:
            self.goto(SCREEN_SERVE_MSG_START)
            self.write("Type s or S to serve the ball", align="center", font=("Courier", 15, "normal"))

        self.goto(SCREEN_BOTTOM_MIDDLE)
        for _ in range(24):
            self.setheading(90)
            self.pendown()      # Put the pen down to draw a dash
            self.forward(15)    # Length of the dash
            self.penup()        # Lift the pen up to leave a gap
            self.forward(10)    # Length of the space
    
        # Type q or Q to quit (on bottom of screen)
        self.goto(SCREEN_BOTTOM_MSG_START)
        self.write("Type q or Q to quit", align="center", font=("Courier", 15, "normal"))




    def point_left(self):
        """Adds a point to the left player and refreshes display."""
        self.left_score += 1
        self.update_scoreboard()

    def point_right(self):
        """Adds a point to the right player and refreshes display."""
        self.right_score += 1
        self.update_scoreboard()