from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, dest):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.penup()
        self.speed("fastest")

        self.goto(dest)
        self.shapesize(stretch_wid=5, stretch_len=1)

    def up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)


    def down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)