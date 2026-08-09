#*****************************************************
# Quiz App:                                          *
# Author:    Keith Caldwell                          *
# Date:      August 8,2026                           *
#*****************************************************
# Description:                                       *
# This task is Day 34 of 100 days of Python:         *
# The purpose of this script is to upgrade a quiz    *
# app (which was previously completed on Day 17,     *
# using a static set of quiz questions).             *
#                                                    *
# This version of the app automatically calls an     *
# API, to get a brand new set of 10 new quiz         *
# questions, every time this quiz is played. It      *
# also keeps score on the screen, and turns screen   *
# color to either green or red (just for a second)   *
# after each question to immediately let the user    *
# know if they got the question right or wrong.      *
#                                                    *
# At the end of the quiz, the ending score will      *
# remain displayed, along with a message advising    *
# the user has completed the quiz.                   *
#                                                    *
# Concepts learned on this task, were further        *
# practice with the Python tinkter GUI elements,     *
# more Object Oriented Programming with the GUI      *
# objects, and continuing to work with calling of    *
# external APIs from Python.                         *
#*****************************************************
import smtplib
from pathlib import *
import os
import requests
import html
import json
import time
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from question_model import Question
# from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

#*****************************************************************
# Parameters are shown below. Further documentation for Open     *
# Trivia API can be found at:                                    *
#                                                                *
# https://opentdb.com/api.php                                    *
#*****************************************************************
parameters = {
    "amount": 10,
    "type": "boolean",
}

# ---------------------------- FUNCTION DEFINITIONS-------------------- #
def get_10_trivia_questions():
    response = requests.get(url="https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()

    data = response.json()
    return data


question_bank = []
data = get_10_trivia_questions()

# Loop directly through the list of question dictionaries
for item in data["results"]:
    question_text =     item["question"]
    question_text =     html.unescape(question_text)
    question_answer =   item["correct_answer"]
    question_answer =   html.unescape(question_answer)
    new_question =      Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

#**********************************************************
# Score and "quiz completed message displays on window.   *
# Message below only displays after window is closed.     *
#**********************************************************
print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
