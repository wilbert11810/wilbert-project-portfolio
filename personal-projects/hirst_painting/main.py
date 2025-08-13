# import colorgram
#
# rgb = []
# colors = colorgram.extract("image.jpg", 60)
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new = (r ,g, b)
#     rgb.append(new)
# print(rgb)
from turtle import Turtle, Screen
import random
import turtle
from PIL.ImageChops import screen

color_list = [(202, 159, 104), (211, 165, 20), (118, 184, 207), (155, 58, 98), (224, 205, 109), (17, 106, 159), (45, 13, 23), (144, 30, 55), (12, 21, 52), (187, 155, 171), (170, 65, 44), (54, 18, 14), (43, 122, 67), (151, 29, 24), (9, 28, 22), (66, 164, 91), (106, 179, 161), (158, 207, 213), (196, 100, 96), (207, 181, 203), (241, 199, 5), (180, 100, 113), (29, 41, 106), (163, 207, 196), (15, 100, 51), (218, 178, 175), (7, 85, 112), (108, 126, 152), (188, 186, 206), (87, 139, 163)]

tim = Turtle()
screen_time = Screen()
def random_color(set_of_color):
    color = random.choice(color_list)
    return color
turtle.colormode(255)
tim.hideturtle()
x = -300
y = -200
for a in range(10):
    tim.teleport(x, y)
    for a in range(10):
        color = random_color(color_list)
        tim.up()
        tim.forward(50)
        tim.dot(20, color)
    y += 40

screen_time.exitonclick()