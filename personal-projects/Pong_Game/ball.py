from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.move_speed = 0.1
        self.setpos(0, 0)
        self.x_position = 10
        self.y_position = 10

    def move(self):
        new_x = self.xcor() + self.x_position
        new_y = self.ycor() + self.y_position
        self.goto(new_x, new_y)
    def bounce_y(self):
        self.y_position *= -1
    def bound_x(self):
        self.x_position *= -1
        self.move_speed *= 0.9
    def refresh(self):
        self.x_position *= -1
        self.move_speed = 0.1
        self.goto(0,0)
