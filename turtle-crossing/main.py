#*************************************************
# Turtle Crossing Game: Written using Python     *
#                       Turtle.                  *
# Author:    Keith Caldwell                      *
# Date:      July 19,2026                        *
#*************************************************
# Description:                                   *
# This task is day 23 of 100 days of Python:     *
# Mostly building on earlier concepts learned,   *
# however this time the game needs to track      *
# contact with multiple objects - adding a       *
# little more complexity. One of the bigger      *
# challenges in this task, will be keeping       *
# track of the list of car objects.              *
#                                                *
# Cars will be generated on the right side of    *
# the screen, and will move towards the left.    *
# They're only relevant when positioned on the   *
# 600 X 600 screen. Therefore, the car manager   *
# will add them to the car list when created,    *
# incrementing each car's position as it moves   *
# across the screen, and then remove each car    *
# from the list, after it's no longer on the     *
# 600 X 600 screen.                              *
#*************************************************
import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

CROSSED_THE_STREET = 280

#*************************************************
# Function definitions are shown below.          *
#*************************************************
# Keeps track of which keys are currently held down
keys = {
    "Up": False,
    "Down": False,
    "Quit": False
}

# Controls Up/Down for right paddle
def press_up():      keys["Up"] = True
def release_up():    keys["Up"] = False
def press_down():    keys["Down"] = True
def release_down():  keys["Down"] = False
def quit_game():     keys["Quit"] = True


#*****************************************************************
# Screen sensing keys and object instantiation is defined below. *
#*****************************************************************
screen = Screen ()
screen.setup(width=600,height=600)
screen.bgcolor("white")
screen.title("Turtle Crossing")
screen.onkeypress(press_up, "Up")
screen.onkeyrelease(release_up, "Up")
screen.onkeypress(press_down, "Down")
screen.onkeyrelease(release_down, "Down")
screen.onkeypress(quit_game, "q")
screen.onkeypress(quit_game, "Q")
screen.listen()
screen.tracer(0)

scoreboard = Scoreboard()
carmanager = CarManager()
player = Player()


while scoreboard.game_is_on:
    time.sleep(0.1)
    if keys["Up"] == True:
        player.move_forward()
    if keys["Down"] == True:
        player.move_backward()
    if keys["Quit"] == True:
        game_is_on = False
    if player.ycor() >= CROSSED_THE_STREET:
        scoreboard.next_level()
        carmanager.increase_car_speed()
        player.goto_start_position()

    carmanager.create_car()
    carmanager.move_cars_forward()
    carmanager.check_if_player_hit(player)
    if carmanager.player_hit:
        scoreboard.game_is_on = False
        scoreboard.update_scoreboard()

    screen.update()

screen.exitonclick()
