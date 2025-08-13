import turtle
import pandas

data = pandas.read_csv("50_states.csv")

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                    prompt="What's another state's name?").title()
    if answer_state == "Exit":
        missing_states = [states for states in all_states if states not in guessed_states]
        # missing_states = []
        # for state in all_states:
        #     if state not in guessed_states:
        #         missing_states.append(state)
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()

# words = turtle.Turtle()
# words.penup()
# words.hideturtle()
# list_answer = []
# result = 0
# while result < 50:
#     answer_state = screen.textinput(title=f"{result}/50 States Correct", prompt="What's another state's name?").title()
#     if not data[data["state"] == answer_state].empty and answer_state not in list_answer:
#         list_answer.append(answer_state)
#         result += 1
#         answer_received = data[data["state"] == answer_state]
#         x_coordinate = answer_received["x"].iloc[0]
#         y_coordinate = answer_received["y"].iloc[0]
#
#         words.goto(x_coordinate, y_coordinate)
#         words.write(answer_state)
#
#
# turtle.mainloop()


# screen.exitonclick()