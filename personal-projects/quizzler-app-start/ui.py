from tkinter import *
import tkinter.messagebox
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, pady=20, padx=20)
        self.score = Label(text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score.grid(row=0, column=1)
        self.canvas = Canvas(width=300, height=250, highlightthickness= 0, bg="white")
        self.text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Hello",
            font=("Arial", 20, "italic"),
            fill=THEME_COLOR
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)



        true = PhotoImage(file='./images/true.png')
        false = PhotoImage(file="./images/false.png")
        self.true_button = Button(image=true, highlightthickness=0, command=self.check_button)
        self.false_button = Button(image=false, highlightthickness=0, command=self.wrong_button)
        self.true_button.grid(row=2, column=0)
        self.false_button.grid(row=2, column=1)
        self.get_next_question()


        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():

            self.score.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.text, text=q_text)
        else:
            self.canvas.itemconfig(self.text, text="You have reached the end of the quiz...")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def check_button(self):
        check = self.quiz.check_answer("True")
        self.give_feeback(check)


    def wrong_button(self):
        check = self.quiz.check_answer("False")
        self.give_feeback(check)


    def give_feeback(self, check):
        if check:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000,self.get_next_question)
