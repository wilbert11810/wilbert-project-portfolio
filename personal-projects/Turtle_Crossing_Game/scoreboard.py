FONT = ("Courier", 24,  "normal")
from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()

        self.hideturtle()
        self.penup()
        self.color("black")
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-280, 250)
        self.write(f"Level: {self.score}", align="left", font=FONT)

    def game_over(self):
        self.goto(0,0)
        self.write("Game Over", align="center", font=FONT)