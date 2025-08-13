from idlelib.debugobj import myrepr
from tkinter import TkVersion
from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
my_timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(my_timer)
    canvas.itemconfig(timer_text, text="00:00")
    checkmark["text"] = ''
    title.config(text="Timer")
    global REPS
    REPS = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS
    REPS += 1
    work_sec =  WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 8 == 0:
        count_down(long_break_sec)
        title.config(text="Long Break", fg=RED)
    elif REPS % 2 == 0:
        count_down(short_break_sec)
        title.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title.config(text="Work", fg=GREEN)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global my_timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        my_timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if REPS % 2 == 0:
            checkmark["text"] += "✓"



# ---------------------------- UI SETUP ------------------------------- #



window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100,112, image=tomato_img)
timer_text = canvas.create_text(100,130, text="00:00", fill="white", font=(FONT_NAME, 16, "bold"))
canvas.grid(column=1,row=1)


#Label
title = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
title.grid(column=1,row=0)

checkmark = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME,14, "normal"))
checkmark.grid(column=1, row=2)
checkmark.config(padx=20, pady=20)

#Button
start = Button(text='Start', highlightthickness=0, width=5, command=start_timer)
start.grid(column=0, row=2)

reset = Button(text="Reset", highlightthickness=0, width=5, command=reset_timer)
reset.grid(column=2, row=2)




window.mainloop()