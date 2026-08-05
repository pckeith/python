#*****************************************************
# Birthday Email Scheduler:                          *
# Author:    Keith Caldwell                          *
# Date:      August 4,2026                           *
#*****************************************************
# Description:                                       *
# This task is Day 32 of 100 days of Python:         *
# Todays task was to build 2 apps which would make   *
# use of the Python smtplib library. The SMTP        *
# acronym stands for: Simple Mail Transfer Protocol. *
# This script sends out automated birthday emails.   *
#                                                    *
# For anyone interested in email protocols, there    *
# are 4 main programs (SMTP, POP3, IMAP, and         *
# Webmail), and I've included an overview of each    *
# at the bottom of this program description, to help *
# you understand major email components. However,    *
# today's Pythons task will be focused on SMTP,      *
# which is just the sending of emails.               *
#                                                    *
# While testing sending emails using SMTP, I         *
# discovered something which I didn't even see       *
# documented in the 100 days Python course: I        *
# discovered my ISP (and many others, I'm told)      *
# will block traffic for port 25, which is the       *
# default port for SMTP. Therefore (as you'll see    *
# in the solution I built below) it's a good idea    *
# to instead use SMTP_SSL (with port 465, as I did   *
# below), or else just use SMTP (with port 587).     *
# You'll also see this in code I've included         *
# (but commented out) below.                         *
#                                                    *
#---------- EMAIL PROGRAMS OVERVIEW: ----------------*
#                                                    *
# SMTP (Simple Mail Transfer Protocol):              *
# Sends email from a device to the mail server, or   *
# passes it between different servers.               *
#                                                    *
#   How it works: Acts like a digital mail carrier   *
#                 for outbound messages. It only     *
#                 handles sending, not receiving.    *
#                                                    *
# POP3 (Post Office Protocol version 3):             *
# Downloads emails from a server to local device.    *
#                                                    *
#   How it works: Like picking up mail at the post   *
#                 office and taking it home. It      *
#                 usually deletes the copy from the  *
#                 server once downloaded, saving     *
#                 server space, but making it more   *
#                 difficult to read the same mail    *
#                 across multiple devices.           *
#                                                    *
#  IMAP (Internet Message Access Protocol):          *
#  Reads & syncs emails directly on mail server.     *
#                                                    *
#   How it works: Leaves messages on the server to   *
#                 alow viewing the same inbox        *
#                 across multiple devices (phone,    *
#                 tablet, computer). If you delete   *
#                 an email on one device, it         *
#                 disappears everywhere.             *
#                                                    *
#  Webmail:                                          *
#  Provides a website interface (like Gmail or       *
#  Outlook on the web) to manage your email.         *
#                                                    *
#   How it works: Uses a web browser instead of a    *
#                 separate mail app on your phone    *
#                 or computer. It connects directly  *
#                 to the server behind the scenes,   *
#                 functioning similarly to an IMAP   *
#                 setup.                             *
#                                                    *
#*****************************************************
import smtplib
from pathlib import *
import os
import random
import csv
import pandas as pd
from email.message import EmailMessage
import datetime as dt

SMTP_SERVER = "smtp.yourdomain.com"
SMTP_PORT = 465  # Switched to SSL port (Note: 587 works for plain SMTP connection)
SENDER_EMAIL = "your_name@yourdomain.com"
SENDER_PASSWORD = "your_password"


now = dt.datetime.now()
year_now = now.year
month_now = now.month
day_now = now.day
day_of_week_now = now.weekday() #Note: Result is a number, starting at 0 (Monday)


#***********************************************************
# Get the list of emails to check for today's birthday.    *
#***********************************************************
script_dir = f"{Path(__file__).resolve().parent}{os.sep}"
birthday_email_file = "birthday_email_list.csv"
birthday_email_file_path = str(Path(script_dir) / birthday_email_file)
df = pd.read_csv(birthday_email_file_path)
birthday_email_list = df.values.tolist()

for name,email,email_type,year,month,day in birthday_email_list:

    if ((year == year_now) and (month == month_now) and (day == day_now)):
        print(f"{name},{email},{email_type},{year},{month},{day}")
        print(f"Happy Birthday {name}!")

        match email_type:
            case 1:
                letter_template_file = "birthday_letter_family.txt"
            case 2:
                letter_template_file = "birthday_letter_friend.txt"
            case 3:
                letter_template_file = "birthday_letter_romantic.txt"
            case _:
                letter_template_file = "unknown" 


        if (letter_template_file != "unknown"):

            birthday_email_letter_file = letter_template_file
            birthday_email_letter_file_path = str(Path(script_dir) / "birthday_letter_templates" / birthday_email_letter_file)
            with open(birthday_email_letter_file_path, 'r', encoding='utf-8') as file:
                birthday_email_letter = file.read()

            birthday_email_letter = birthday_email_letter.replace("[email_name]", name)
            birthday_email_letter = birthday_email_letter.replace("[my_name]", "Bob (my name)")

            msg = EmailMessage()
            msg["Subject"] = f"Happy Birthday {name}!"
            msg["From"] = SENDER_EMAIL
            msg["To"] = email
            msg.set_content(f"{birthday_email_letter}")

            try:
                #*************************************************************************
                # Note: We're using SMTP_SSL, but can use SMTP for port 587 as follows:  *
                # with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:               *
                #*************************************************************************
                # Use SMTP_SSL for port 465
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as connection:
                    connection.login(SENDER_EMAIL, SENDER_PASSWORD)
                    connection.send_message(msg)
                    print("Email sent successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")