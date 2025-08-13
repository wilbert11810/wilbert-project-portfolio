from turtle import Screen
from player import Player, FINISH_LINE_Y
from scoreboard import Scoreboard
from car_manager import CarManager
import time

screen = Screen()

screen.setup(width=600, height=600)
screen.tracer(0)
turtle = Player()
scoreboard = Scoreboard()
car_manager = CarManager()
screen.listen()
screen.onkey(turtle.move_up, "Up")
game_is_on = True
r = 0
while game_is_on:
    screen.update()
    time.sleep(0.1)
    if r % 2 == 0:
        car_manager.create_car()
    car_manager.move_up()
    for car in car_manager.all_cars:
        if car.distance(turtle) < 20:
            scoreboard.game_over()
            game_is_on = False
            break

    if turtle.ycor() == FINISH_LINE_Y:
        turtle.reset()
        scoreboard.score += 1
        car_manager.increment_move()
        scoreboard.update_scoreboard()
    r += 1

screen.exitonclick()