#*************************************************
# Pong game: Written in Python Turtle            *
# Author:    Keith Caldwell                      *
# Date:      July 18,2026                        *
#*************************************************
# Description:                                   *
# This task is part of a 100 day Python boot     *
# camp course I've been taking recently. In the  *
# first 30 days of the course, we're using the   *
# Python Turtle class a lot, as in this game.    *
#                                                *
# However, on each new task we're getting a bit  *
# more sophisticated. In this example, I         *
# continued creating Python classes, also        *
# implemented loop control with screen.ontimer.  *
# Finally, I used Try / Except Terminator logic  *
# to exit cleanly from the game loop when using  *
# q or Q to quit the game.                       *
#*************************************************

CENTER_OF_SCREEN = (0,0)

from turtle import Screen, Terminator
from scoreboard import Scoreboard
from ball import Ball
from left_paddle import Left_Paddle
from right_paddle import Right_Paddle


#*************************************************
# Function definitions are shown below.          *
#*************************************************
# Keeps track of which keys are currently held down
keys = {
    "Up": False,
    "Down": False,
    "greater": False,
    "<": False,
    "Serve": False
}

# Controls Up/Down for left paddle
def press_lt():      keys["<"] = True
def release_lt():    keys["<"] = False
def press_gt():      keys["greater"] = True
def release_gt():    keys["greater"] = False
# Controls Up/Down for right paddle
def press_up():      keys["Up"] = True
def release_up():    keys["Up"] = False
def press_down():    keys["Down"] = True
def release_down():  keys["Down"] = False
# Serve ball after point
def serve():         keys["Serve"] = True
# Main game loop
def game_loop():
    
    try:
        # Handle the left and right player paddle movements
        if keys["greater"]:
            left_paddle.up()
        if keys["<"]:
            left_paddle.down()

        if keys["Up"]:
            right_paddle.up()
        if keys["Down"]:
            right_paddle.down()

        if scoreboard.print_type_s_to_serve == True:
            if keys["Serve"] == True:
                ball.goto(CENTER_OF_SCREEN)
                ball.showturtle()
                ball.is_moving = True
                keys["Serve"] = False 
                scoreboard.print_type_s_to_serve = False
                scoreboard.update_scoreboard()

        # Move the ball
        if ball.is_moving:
            ball.move()

        # Bounce off Left paddle (300 - half ball width)
        if ball.xcor() < -280:
            left_paddle_hit = False
            for segment in left_paddle.left_paddle[1:]:
                if (ball.distance(segment) < 20):
                    left_paddle_hit = True
            if left_paddle_hit == True:
                ball.bounce_off_side()
            else:
                ball.setx(-280)
                ball.is_moving = False
                ball.hideturtle()
                scoreboard.print_type_s_to_serve = True
                scoreboard.point_right()

        # Bounce off Right paddle (300 - half ball width)
        if ball.xcor() > 278:
            right_paddle_hit = False
            for segment in right_paddle.right_paddle[1:]:
                if (ball.distance(segment) < 20):
                    right_paddle_hit = True
            if right_paddle_hit == True:
                ball.bounce_off_side()
            else:
                ball.setx(278)
                ball.is_moving = False
                ball.hideturtle()
                scoreboard.print_type_s_to_serve = True
                scoreboard.point_left()

            
        # Bounce off Top/Bottom walls
        if ball.ycor() > 288 or ball.ycor() < -280:
            ball.bounce_off_top_bottom()
        
        screen.update()
        screen.ontimer(game_loop, 10)
    
    except Terminator:
        # Window closed via 'q' or 'Q'; exit cleanly without error
        pass


#*****************************************************************
# Screen sensing keys and object instantiation is defined below. *
#*****************************************************************
screen = Screen ()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0) 
screen.onkeypress(press_gt, ".")
screen.onkeyrelease(release_gt, ".")
screen.onkeypress(press_lt, ",")
screen.onkeyrelease(release_lt, ",")
screen.onkeypress(press_up, "Up")
screen.onkeyrelease(release_up, "Up")
screen.onkeypress(press_down, "Down")
screen.onkeyrelease(release_down, "Down")
screen.onkeypress(screen.bye, "q")
screen.onkeypress(screen.bye, "Q")
screen.onkeypress(serve, "s")
screen.onkeypress(serve, "S")
screen.listen()

scoreboard = Scoreboard()
ball = Ball()
left_paddle = Left_Paddle()
right_paddle = Right_Paddle()


#*****************************************************************
# game_loop()       - starts the first frame of the game loop.   *
# screen.mainloop   - Keeps window open, listening for events.   *
#*****************************************************************
game_loop()
screen.mainloop()

