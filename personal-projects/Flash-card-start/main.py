import tkinter.messagebox
from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40 , "bold")
FONT = ("Arial", 60, "bold")

try:
    df = pd.read_csv("./data/words_to_learn.csv")
    if df.empty:
        df = pd.read_csv("./data/french_words.csv")
except FileNotFoundError :
    df = pd.read_csv("./data/french_words.csv")
except pd.errors.EmptyDataError:
    df = pd.read_csv("./data/french_words.csv")

french_dict = df.to_dict(orient="records")
current_card = {}
def french_language():
    global current_card, after_card
    window.after_cancel(after_card)
    if len(french_dict) < 1:
        completed()
        return
    current_card = random.choice(french_dict)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_words, text="French", fill="black")
    canvas.itemconfig(words, text=current_card["French"])
    after_card = window.after(3000, flip_card)

def completed():
    tkinter.messagebox.showinfo(title="Congratulations", message="You successfully learn the whole card.")

def flip_card():
    canvas.itemconfig(canvas_image, image= card_back)
    canvas.itemconfig(title_words, text="English", fill="white")
    canvas.itemconfig(words, text=current_card["English"])

def save_progress():
    french_dict.remove(current_card)
    df = pd.DataFrame(french_dict)
    df.to_csv("./data/words_to_learn.csv", index=False)
    french_language()


#UI Setup
window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)
after_card = window.after(3000,flip_card)

#card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400,263, image=card_front)
title_words = canvas.create_text(400,150, text="French", font=TITLE_FONT)
words = canvas.create_text(400,263, text="Trouve", font=FONT)
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=french_language)
wrong_button.grid(row=1,column=0)

correct_img = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_img, highlightthickness=0, command=save_progress)
correct_button.grid(row=1,column=1)

french_language()
window.mainloop()