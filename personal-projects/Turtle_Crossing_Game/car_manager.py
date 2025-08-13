COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
from turtle import Turtle
import random

class CarManager:
    def __init__(self):
        self.all_cars = []
        self.move_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        if random.randint(1, 3) == 1:
            car = Turtle()
            car.penup()
            car.shape("square")
            car.shapesize(stretch_wid=1, stretch_len=1.5)
            car.setheading(180)
            car.color(random.choice(COLORS))
            car.goto(300, random.randint(-220, 220))
            self.all_cars.append(car)




    def move_up(self):
        for car in self.all_cars:
            car.forward(self.move_speed)
            if car.xcor()  < -300:
                car.hideturtle()
                self.all_cars.remove(car)


    def increment_move(self):
        self.move_speed += MOVE_INCREMENT
