#*****************************************************
# Check Twilio sent msg status:                      *
# Author:    Keith Caldwell                          *
# Date:      August 11,2026                          *
#*****************************************************
# Description:                                       *
# This script is related to the Twilio message       *
# portion of the main.py program for Day 35:         *
#                                                    *
# I discovered there was a bit more to setting up    *
# a Twilio account to send a real SMS message to a   *
# real phone, than I originally thought. To send     *
# messages in the USA, it turns out you need to pay  *
# Twilio $20 minimum to setup a basic paid account,  *
# and then you need to also select a paid number,    *
# which will cost $1.15 a month to hold (whether you *
# send texts or not - sending texts will cost you    *
# around 2 cents per text in the USA). In USA,       *
# you're also not permitted to send SMS texts unless *
# you go through the following four steps to         *
# properly register your brand, as follows:          *
#                                                    *
# 1) Set up a compliance profile                     *
# 2) Select a messaging service.                     *
# 3) Set up an A2P Brand registration.               *
# 4) Set up an A2P Campaign registration.            *
#                                                    *
# Running the Python code below will helps to        *
# report on any errors associated with a             *
# message.sid, after sending a message from the      *
# main.py script.                                    *
#                                                    *
# Note: the message could have appeared to have      *
# been successfully sent after running the main.py   *
# script, however you have to parse the message.sid  *
# after running the main.py script - to see any      *
# hidden problems. Some problems, for example,       *
# could be not properly going through the four       *
# steps mentioned above.                             *
#                                                    *
# If you modify this script to add your ACCOUNT_SID, *
# AUTH_TOKEN, and the message.sid received from      *
# running the main.py program, this script should    *
# provide details as to what's going on, whether the *
# message just hasn't come through yet, or if your   *
# account actually has a configuration problem.      *
#*****************************************************
from twilio.rest import Client

ACCOUNT_SID="Your Account SID"
AUTH_TOKEN="Your Account Secret"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Fetch the current state of the message (message.sid from main.py)
msg = client.messages("message.sid from main.py").fetch()

print(f"Current Status: {msg.status}")
if msg.error_code:
    print(f"Error Code: {msg.error_code}")
    print(f"Error Message: {msg.error_message}")