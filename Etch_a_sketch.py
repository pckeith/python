#***********************************************
# Etch a sketch game (using Python Turtle):    *
#***********************************************
#     This game emulates the classic Etch A    *
#     Sketch game, originally created by the   *
#     Ohio Art company in 1960.                *
#                                              *
#     Here's all you need to run this code:    *
#                                              *
#     1) Make sure Python 3 is installed       *
#        on your computer.                     *
#     2) Run this code on a Python IDE, such   *
#        as VS Code, or PyCharm.               *
#     3) Use the following keys to move the    *
#        cursor (pen) around, and/or control   *
#        the game:                             *
#                                              *
#        space bar= move forward in whatever   *
#                   direction the cursor is    *
#                   already pointing.          *
#                                              *
#        Arrow keys:                           *
#            Right arrow - Move right.         *
#            Left arrow  - Move left.          *
#            Up arrow    - Move up.            *
#            Down arrow  - Move down.          *
#                                              *
#        "<" and ">" keys:                     *
#            ">" key     - Draw clockwise      *
#                          circular pattern.   *
#                          Note: Remember to   *
#                                use the shift *
#                                key!          *
#            "<" key     - Draw counter-       *
#                          clockwise circular  *
#                          pattern.            *
#                          Note: Remember to   *
#                                use the shift *
#                                key!          *
#                                              *
#        "c" or "C" key:                       *
#            Clear the screen, and put the     *
#            cursor back in the center.        *
#                                              *
#        "q" or "Q" key:                       *
#            Quit the program.                 *
#                                              *
#***********************************************
from turtle import Turtle, Screen
import time
import tkinter.messagebox as msgbox

screen = Screen()
screen.tracer(0)  # Turns off auto-animation updates for smooth movement
screen.setup(width=600, height=600)


#***********************************************
# 1. Key state tracking dictionary             *
#***********************************************
# Keeps track of which keys are currently held down
keys = {
    "space": False,
    "Up": False,
    "Down": False,
    "Left": False,
    "Right": False,
    "greater": False,
    "c": False,
    "<": False,
}


#***********************************************
# 2. Define all game-related functions         *
#***********************************************
def press_space():    keys["space"] = True
def release_space():  keys["space"] = False

def press_up():    keys["Up"] = True
def release_up():  keys["Up"] = False

def press_down():    keys["Down"] = True
def release_down():  keys["Down"] = False

def press_left():    keys["Left"] = True
def release_left():  keys["Left"] = False

def press_right():    keys["Right"] = True
def release_right():  keys["Right"] = False

def press_lt():    keys["<"] = True
def release_lt():  keys["<"] = False

def press_gt():    keys["greater"] = True
def release_gt():  keys["greater"] = False

def press_clear():    keys["c"] = True
def release_clear():  keys["c"] = False

def move_forward(player):
    player.forward(10)

def move_up(player):
    player.setheading(90)
    player.forward(10)

def move_down(player):
    player.setheading(270)
    player.forward(10)
def move_left(player):
    player.setheading(180)
    player.forward(10)

def move_right(player):
    player.setheading(0)
    player.forward(10)

def clockwise_circle(player):
    player.right(10)
    player.forward(10)

def counter_clockwise_circle(player):
    player.left(10)
    player.forward(10)

def clear_screen_and_center(player):
    player.penup()
    player.clear()
    player.home()
    player.pendown()

def exit_game():
    screen.bye()

#***********************************************
# 3. game_loop controls the game iteration     *
#    Note: control keys are not mutually       *
#          selective. This allows you to go    *
#          faster, by selecting more than one  *
#          key!                                *
#***********************************************
def game_loop(player):
    if keys["space"]:
        move_forward(player)
    if keys["Up"]:
        move_up(player)
    if keys["Down"]:
        move_down(player)
    if keys["Left"]:
        move_left(player)
    if keys["Right"]:
        move_right(player)
    if keys["greater"]:
        clockwise_circle(player)
    if keys["<"]:
        counter_clockwise_circle(player)
    if keys["c"]:
        clear_screen_and_center(player)

    #****************************************************************
    # Check Y Conditions: Make sure player stays on the screen!     *    
    #****************************************************************
    if player.ycor() >= 295:
        player.setpos(player.xcor(),295)
        player.setheading(0)
        player.forward(10)
    elif player.ycor() <= -290:
        player.setpos(player.xcor(),-290)
        player.setheading(180)
        player.forward(10)
    #****************************************************************
    # Check X Conditions: Make sure player stays on the screen!     *    
    #****************************************************************
    if player.xcor() >= 290:
        player.setpos(290,player.ycor())
        player.setheading(270)
        player.forward(10)
    elif player.xcor() <= -295:
        player.setpos(-295,player.ycor())
        player.setheading(90)
        player.forward(10)

    screen.update()  # Manually refresh the screen frame
    screen.ontimer(lambda: game_loop(player), 50) 


#***********************************************
# 4. Bind events to the screen listeners       *
#***********************************************
screen.onkeypress(press_space, "space")
screen.onkeyrelease(release_space, "space")

screen.onkeypress(press_up, "Up")
screen.onkeyrelease(release_up, "Up")

screen.onkeypress(press_down, "Down")
screen.onkeyrelease(release_down, "Down")

screen.onkeypress(press_left, "Left")
screen.onkeyrelease(release_left, "Left")

screen.onkeypress(press_right, "Right")
screen.onkeyrelease(release_right, "Right")

screen.onkeypress(press_gt, "greater")
screen.onkeyrelease(release_gt, "greater")

screen.onkeypress(press_lt, "<")
screen.onkeyrelease(release_lt, "<")

screen.onkeypress(press_clear, "c")
screen.onkeyrelease(release_clear, "c")
screen.onkeypress(press_clear, "C")
screen.onkeyrelease(release_clear, "C")

screen.onkeypress(exit_game, "q")
screen.onkeypress(exit_game, "Q")

# Tell the screen to listen to the keyboard
# events listed above.
screen.listen()


#***********************************************
# 5. Start the Game Engine                     *
#                                              *
#    Note: You can modify the shape parameter  *
#          below, to use any of these shapes   *
#          for your cursor:                    *
#                                              *
#          "classic":  Narrow arrowhead.       *
#          "arrow":    Filled triangle.        *
#          "turtle":   Turtle outline.         *
#          "circle":   Solid circle.           *
#          "square":   Solid square.           *
#          "triangle": Equilateral triangle.   *
#                                              *
#***********************************************
player = Turtle()
player.shape("classic")

msgbox.showinfo("Welcome!", "Etch A Sketch: The cursor will begin as a narrow arrowhead showing in the center of the screen. You can control it like the original Etch a Sketch, using the arrow keys (up, down, left, right) to draw patterns across the screen. You can use the '<' or '>' keys to draw circlar (clockwise or counter-clockwise) patterns. Type 'c' to center and re-draw, or 'q' to quit the game. Click OK to continue. ")
game_loop(player)
screen.mainloop()
