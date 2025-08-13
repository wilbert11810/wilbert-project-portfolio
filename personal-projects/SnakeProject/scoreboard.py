from turtle import Turtle
ALIGNMENT = "center"
FONT = ('Courier', 15, 'bold')
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.speed("fastest")
        self.goto(0,275)
        self.result = 0
        with open("data.txt") as data:
            self.high_score = int(data.read())
        self.update_scoreboard()
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.result} High Score: {self.high_score}", False, ALIGNMENT, font=FONT)


    def reset(self):
        if self.result > self.high_score:
            self.high_score = self.result
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
        self.result = 0
        self.update_scoreboard()

        
    # def game_over(self):
    #     self.goto(0,0)
    #     self.write("GAME OVER", False, ALIGNMENT, FONT)
    def add_point(self):
        self.result += 1
        self.update_scoreboard()