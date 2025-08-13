from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)
l_paddle = Paddle((-350, 0))
r_paddle = Paddle((350, 0))
ball = Ball()
scoreboard = Scoreboard()


screen.listen()
screen.onkey(l_paddle.up, "Up")
screen.onkey(l_paddle.down, "Down")
screen.onkey(r_paddle.up, "w")
screen.onkey(r_paddle.down, "s")


game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    #Detect collision with r_paddle
    if ball.distance(r_paddle)< 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bound_x()
    #detect R paddle misses
    elif ball.xcor() > 350:
        ball.refresh()
        scoreboard.l_point()
        #ball.increase_speed()

    # detect R paddle misses
    elif ball.xcor() < -350:
        ball.refresh()
        scoreboard.r_point()
        #ball.increase_speed()




screen.exitonclick()