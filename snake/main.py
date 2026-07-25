#*************************************************
# Snake Game (with OOP and High Score):          *
# Author:    Keith Caldwell                      *
# Date:      July 17,2026                        *
#*************************************************
# Description:                                   *
# For Day 21 of the 100 Day Python boot camp,    *
# we did the Snake game:                         *
#                                                *
# This is the classic Snake game you may have    *
# played previously in some video arcade, or     *
# (I've been told) on some very old Nokia        *
# "Brick" phones. You navigate the snake around  *
# using the arrow keys, with an objective of     *
# gaining more points by eating more food. The   *
# problem with eating more food, however, is     *
# the snake's tail gets longer and longer,       *
# eventually  becoming impossible not to run     *
# into it.                                       *
#                                                *
# The snake is self-powered. The only thing the  *
# player needs to do, is to keep the snake       *
# moving forward, and not either running into a  *
# wall, or running into it's own tail. Sounds    *
# simple, right? Give this one a shot and you'll *
# see how challenging it can be!                 *
#*************************************************
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import tkinter.messagebox as msgbox
import time


screen = Screen()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0) 


#***********************************************
# 1. Functions are defined below.              *
#***********************************************
def game_loop(snake,game_on):
    
    snake.move_forward()

    # Detect snake eating food
    if (snake.head.distance(food) < 15):
        food.snake_eats_food()
        snake.extend()
        scoreboard.add_one_point()

    # Detect snake collision with wall
    if ((abs(snake.head.xcor()) > 295) or(abs(snake.head.ycor()) > 295)):
        scoreboard.game_over()
        game_on = False

    # Detect snake collision with itself
    for segment in snake.snake[1:]:
        if (snake.head.distance(segment) < 10):
            scoreboard.game_over()
            game_on = False

    screen.update()
    # time.sleep(.05)

    # Repeatedly call game_loop every 100ms if game is on
    if game_on:
        screen.ontimer(lambda: game_loop(snake,game_on), 100)

def exit_game():
    screen.bye()


#***********************************************
# 2. Main body of the program is below.        *
#***********************************************
scoreboard = Scoreboard()
screen.update()
game_on = True

msgbox.showinfo("Welcome!", "Snake Game: Move the Snake using the arrow keys... Type 'q' to quit the game. Click OK to continue. ")
snake = Snake()
food = Food()
screen.update()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onkeypress(exit_game, "q")
screen.onkeypress(exit_game, "Q")

game_loop(snake,game_on)

# CRITICAL: This keeps the window open and processing events
screen.mainloop()