from tkinter import *
from pathlib import *
import os
import time
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self,quiz_brain:QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20,pady=20,bg=THEME_COLOR)

        self.frame = Frame(self.window,padx=20,pady=20,bg=THEME_COLOR)
        self.frame.grid(row=3, column=2)
        script_dir = f"{Path(__file__).resolve().parent}{os.sep}"

        self.score_label = Label(text="Score: 0/0", fg="white", bg=THEME_COLOR, font=("Arial", 12))
        self.score_label.grid(row=0, column=1, pady=(0, 20))

        self.canvas = Canvas(width=350,height=250,bg="white",highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150,125,text="Some Question Text",
            fill=THEME_COLOR, font=("Arial",20,"italic"), width=310 )
        self.canvas.grid(row=1,column=0,columnspan=2,sticky="nsew", pady=(0, 30))

        true_button_filename = "true.png"
        true_button_filename_path = str(Path(script_dir) / "images" / true_button_filename)
        self.true_image = PhotoImage(file=true_button_filename_path)
        self.true_button = Button(image=self.true_image, highlightthickness=0, bd=0, command=self.true_button_pressed)   
        self.true_button.grid(row=2, column=0)

        false_button_filename = "false.png"
        false_button_filename_path = str(Path(script_dir) / "images" / false_button_filename)
        self.false_image = PhotoImage(file=false_button_filename_path)
        self.false_button = Button(image=self.false_image, highlightthickness=0, bd=0, command=self.false_button_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've completed the quiz!!")

    def true_button_pressed(self):
        am_i_right = self.quiz.check_answer(user_answer="True")
        self.give_feedback(am_i_right)

    def false_button_pressed(self):
        am_i_right = self.quiz.check_answer(user_answer="False")
        self.give_feedback(am_i_right)

    def give_feedback (self,am_i_right):
        if self.quiz.still_has_questions():
            self.quiz.total += 1
            if am_i_right == True:
                self.quiz.score += 1
                self.canvas.configure(bg="green")
            else:
                self.canvas.configure(bg="red")
            self.score_label.configure(text=f"score: {self.quiz.score}/{self.quiz.total}")

            self.window.after(1000, self.reset_and_continue)

    def reset_and_continue(self):
        self.canvas.configure(bg="white")
        self.get_next_question()