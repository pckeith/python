from turtle import Turtle
import random
import time

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    
    def __init__(self):
        super().__init__()
        self.all_cars = []
        self.player_hit = False
        self.move_distance = STARTING_MOVE_DISTANCE


    def create_car(self):
        # 1-in-6 chance every time the main game loop runs
        if random.randint(1, 6) == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            new_car.goto(300, random.randint(-250, 250))
            self.all_cars.append(new_car)


    def move_cars_forward(self):

        # Move the cars forward (from right to left)
        for car in self.all_cars:
            car.backward(self.move_distance)

        # Safely remove cars that went off the screen using list comprehension
        self.all_cars = [car for car in self.all_cars if car.xcor() > -320]


    def increase_car_speed(self):
        self.move_distance = self.move_distance + MOVE_INCREMENT


    def check_if_player_hit(self,player):
        # Detect car collision with player using a bounding box check
        for car in self.all_cars:
            # Calculate absolute distance on x and y axes
            x_distance = abs(car.xcor() - player.xcor())
            y_distance = abs(car.ycor() - player.ycor())
            
            # Car width is 40 (half is 20), Player width is 20 (half is 10) -> Total X collision zone = 30
            # Car height is 20 (half is 10), Player height is 20 (half is 10) -> Total Y collision zone = 20
            # We subtract 1 pixel as a safety buffer, for a cleaner game feel
            if x_distance < 29 and y_distance < 19:
                self.player_hit = True
                break # Stop checking once a collision is found

