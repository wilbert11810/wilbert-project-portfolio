STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280
from turtle import Turtle

class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.starting_point = STARTING_POSITION
        self.penup()
        self.color("black")
        self.shape("turtle")
        self.goto(STARTING_POSITION)
        self.setheading(90)

    def move_up(self):
        self.forward(MOVE_DISTANCE)

    def reset(self):
        self.goto(STARTING_POSITION)
