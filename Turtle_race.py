#***********************************************
# Turtle Race:                                 *
#***********************************************
#     This game will create 7 turtles, each    *
#     with a different color of the rainbow:   *
#     ("red","orange","yellow","green",        *
#      "blue","RoyalBlue", and "purple")       *
#                                              *
#     Here's all you need to run this code:    *
#                                              *
#     1) Make sure Python 3 is installed       *
#        on your computer.                     *
#     2) Run this code on a Python IDE, such   *
#        as VS Code, or PyCharm.               *
#                                              *
#     When the program starts, a text box      *
#     will appear,asking you to bet on one of  *
#     the 7 turtle colors.                     *
#                                              *
#     - After you make a bet, the turtles will *
#       line up, and begin the race.           *
#     - They will go in all kinds of crazy     *
#       directions, as long as it's not        *
#       backwards, and not off the screen.     *
#     - The first turtle which makes it first  *
#       to any point on the right side of the  *
#       screen wins!                           *
#                                              *
#***********************************************
from turtle import Turtle, Screen, Terminator
import time
import random
import tkinter.messagebox as msgbox

screen = Screen()
screen.tracer(0)  # Turns off auto-animation updates for smooth movement
screen.setup(width=600, height=600)

# Global control variable to manage game loop execution
race_on = True


#***********************************************
# 1. Global data structures used in this       *
#    program.                                  *
#***********************************************
allowed_moves = [
    "space",
    "Up",
    "Down",
    "Right",
    "greater",
    "<"
]

#***********************************************
# 2. Define all game-related functions         *
#***********************************************
def move_forward(player):
    player.forward(10)

def move_up(player):
    player.setheading(90)
    player.forward(20)
    player.setheading(0)

def move_down(player):
    player.setheading(270)
    player.forward(20)
    player.setheading(0)

def move_right(player):
    player.setheading(0)
    player.forward(10)

def clockwise_circle(player):
    player.right(10)
    player.forward(20)
    player.setheading(0)

def counter_clockwise_circle(player):
    player.left(10)
    player.forward(20)
    player.setheading(0)

def clear_screen_and_center(player):
    player.penup()
    player.clear()
    player.home()
    player.pendown()

def exit_game():
    global race_on
    race_on = False  # Tells game loop to stop immediately
    
    # Safely clear turtles to prevent background errors
    try:
        for player in players:
            player.hideturtle()
    except:
        pass
        
    try:
        screen.bye()
    except:
        pass

def starting_position(players):
    
    # Note: X is horizontal, Y is vertical
    x=-250
    y=150

    screen.tracer(1)  # Turns on tracer for starting placement.
    for player in players:
        
        #*************************************
        # Note: Break out if user quit early *
        #*************************************
        if not race_on: return

        try:
            player.showturtle()
            time.sleep(0.50) 
            player.setpos(x,y)
            y -= 50
            screen.update()
        except (Terminator, Exception):
            return
    time.sleep(1.5)
    screen.tracer(0)  # Turns off tracer after starting placement.

#***********************************************
# 3. game_loop controls the game iteration     *
#***********************************************
def game_loop(players):
    global race_on
    if not race_on:
        return  # Stop executing if the game has been exited

    try:
        for player in players:
            if not race_on: return

            random_key = random.choice(allowed_moves)
            if random_key == "space":
                move_forward(player)
            elif random_key == "Up":
                move_up(player)
            elif random_key == "Down":
                move_down(player)
            elif random_key == "Right":
                move_right(player)
            elif random_key == "greater":
                clockwise_circle(player)
            elif random_key == "<":
                counter_clockwise_circle(player)

            #****************************************************************
            # Check Y Conditions: Make sure turtles stay on the screen,     * 
            #                     and moving forward!                       *
            #****************************************************************
            if player.ycor() >= 280:
                player.setpos(player.xcor(),280)
                player.setheading(0)
            elif player.ycor() <= -280:
                player.setpos(player.xcor(),-280)
                player.setheading(0)

            #****************************************************************
            # Check win condition: Right boundary is X = 300                *
            #****************************************************************
            if player.xcor() >= 280:
                race_on = False
                if (user_bet == player.pencolor()):
                    print(f"You won! Your {player.pencolor()} turtle won the race!")
                    msgbox.showinfo("Notice", f"You won! Your {player.pencolor()} turtle won the race! Click OK, then close screen by selecting X on top right.")
                else:
                    print(f"You lost! {player.pencolor()} won the race. You bet on {user_bet}")
                    msgbox.showinfo("Notice", f"You lost! {player.pencolor()} won the race. You bet on {user_bet}. Click OK, then close screen by selecting X on top right.")
                return

            time.sleep(0.05) 
            screen.update()  # Manually refresh the screen frame

        # Only schedule the next loop if the race is active
        if race_on:
            screen.ontimer(lambda: game_loop(players), 50) 
    except (Terminator, Exception):
        return



#***********************************************
# 4. Bind events to the screen listeners       *
#***********************************************
screen.onkeypress(exit_game, "q")
screen.onkeypress(exit_game, "Q")
screen.listen()


#***********************************************
# 5. Start the Game Engine                     *
#***********************************************
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
player_shape = "turtle"
colors = ["red","orange","yellow","green","blue","RoyalBlue","purple"]
msgbox.showinfo("Welcome!", "7 colored turtles will race from left to right. Please pick 'red','orange','yellow','green','blue','RoyalBlue, or 'purple' on the next screen. If no selection is made, a color will be randomly picked. Enter 'q' to quit the race.")
while True:
    user_bet = screen.textinput(title="Bet on a Turtle", prompt="Which turtle will win the race? Enter a color: ")
    random_color = random.choice(colors)
    if (user_bet == ""):
        user_bet = random_color
    if user_bet in colors:
        break
print(f"User bet on: {user_bet}") # Confirms the bet in your console
screen.listen() # Re-enable keyboard listening after closing popup text box

nbr_of_players = 7
players = []
colors_idx = 0
for _ in range(nbr_of_players):
    new_player = Turtle()
    new_player.shape(player_shape)
    new_player.color(colors[colors_idx])
    new_player.hideturtle()
    new_player.penup()
    players.append(new_player)
    colors_idx += 1

# Wrap the execution block to catch errors if the user exits during setup or early loop
try:
    starting_position(players)
    game_loop(players)
    # CRITICAL: Keeps the window open and processes your background game_loop timers
    screen.mainloop()
except (Terminator, Exception):
    pass