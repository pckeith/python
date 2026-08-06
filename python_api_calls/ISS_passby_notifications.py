#*****************************************************
# ISS Space Station Position:                        *
# Author:    Keith Caldwell                          *
# Date:      August 5,2026                           *
#*****************************************************
# Description:                                       *
# This task is Day 33 of 100 days of Python:         *
# The purpose of this script is to send an email     *
# notification if the ISS Space stations comes       *
# close to a specified geograpy. Therefore, there    *
# are 3 things this script needs to do, which are:   *
#                                                    *
# 1) Check today's sunrise / sunset times (from the  *
#    sunrise-sunset.org API), to verify we're        *
#    currently after dark (because you can't see     *
#    the ISS when it passes by during the day).      *
# 2) Continually check for the position of the ISS   *
#    (once per minute), to verify whether it is      *
#    within 5 degrees latitude or longitude of the   *
#    user's position (I am located in the Twin       *
#    Cities, Minnesota - these are the coordinates   *
#    I used).                                        *
# 3) Send an email, when the program determies the   *
#    ISS is within 5 degrees of the user's position. *
#                                                    *
#*****************************************************
import smtplib
from pathlib import *
import os
import requests
import json
import time
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

MY_LATITUDE = 44.8041
MY_LONGITUDE = -93.1669

SMTP_SERVER = "smtp.yourdomain.com"
SMTP_PORT = 465  # Switched to SSL port (Note: 587 works for plain SMTP connection)
SENDER_EMAIL = "your_username@yourdomain.com"
SENDER_PASSWORD = "your_password"

#*****************************************************************
# Parameters are shown below. Note manual date parameters        *
# can be supplied, in format: YYYY-MM-DD, also the "formatted"   *
# parameter determines if the date/time will be formatted or     *
# not. Further documentation for sunrise / sunset API can be     *
# found at:                                                      *
#                                                                *
# https://sunrise-sunset.org/api                                 *
#*****************************************************************

parameters = {
    "lat": MY_LATITUDE,
    "lng": MY_LONGITUDE,
    "formatted": 0
}


# ---------------------------- FUNCTION DEFINITIONS-------------------- #
def get_todays_sunrise_sunsets():
    response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()  # Raise an error for any response other than 200!
    response_text = response.text
    data_dict = json.loads(response_text)
    sunrise = data_dict["results"]["sunrise"]
    sunset = data_dict["results"]["sunset"]
    target_tz = timezone(timedelta(hours=-5))

    sunrise_dt = datetime.fromisoformat(sunrise)
    sunrise_dt = sunrise_dt.astimezone(target_tz)
    # print(f"\nsunrise unformatted= {sunrise_dt}")
    sunrise_year = sunrise_dt.date().year
    sunrise_month = sunrise_dt.date().month
    sunrise_day = sunrise_dt.date().day
    sunrise_hours = sunrise_dt.time().hour
    sunrise_mins = sunrise_dt.time().minute
    sunrise_sec = sunrise_dt.time().second
    print(f"Sunrise Date= {sunrise_year} {sunrise_month} {sunrise_day}: Time= {sunrise_hours} {sunrise_mins} {sunrise_sec}")

    sunset_dt = datetime.fromisoformat(sunset)
    sunset_dt = sunset_dt.astimezone(target_tz)
    # print(f"\nsunset unformatted= {sunset_dt}")
    sunset_year = sunset_dt.date().year
    sunset_month = sunset_dt.date().month
    sunset_day = sunset_dt.date().day
    sunset_hours = sunset_dt.time().hour
    sunset_mins = sunset_dt.time().minute
    sunset_sec = sunset_dt.time().second
    print(f"Sunset Date= {sunset_year} {sunset_month} {sunset_day}: Time= {sunset_hours} {sunset_mins} {sunset_sec}")

    return sunrise_dt, sunset_dt


def get_current_iso_datetime():
    # Get current UTC time in ISO format
    current_dt = datetime.now(timezone.utc).isoformat()
    current_dt = datetime.fromisoformat(current_dt)
    target_tz = timezone(timedelta(hours=-5))
    current_dt = current_dt.astimezone(target_tz)
    # print(f"\ncurrent unformatted= {current_dt}")
    current_year = current_dt.date().year
    current_month = current_dt.date().month
    current_day = current_dt.date().day
    current_hours = current_dt.time().hour
    current_mins = current_dt.time().minute
    current_sec = current_dt.time().second
    print(f"\nCurrent Date= {current_year} {current_month} {current_day}: Time= {current_hours} {current_mins} {current_sec}")

    return current_dt


def get_iss_current_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # Raise an error for any response other than 200!
    response_text = response.text
    iss_latitude = json.loads(response_text)["iss_position"]["latitude"]
    iss_longitude = json.loads(response_text)["iss_position"]["longitude"]

    return float(iss_latitude), float(iss_longitude)

# ---------------------------- MAIN PROGRAM LOGIC --------------------- #

sunrise_dt, sunset_dt = get_todays_sunrise_sunsets()

print("\nTimer started. Press Ctrl+C to stop.")
try:
    while True:

        #Another minute has passed, get datetime again
        current_dt = get_current_iso_datetime()
        current_hour = current_dt.hour
        sunrise_hour = sunrise_dt.hour
        sunset_hour = sunset_dt.hour

        if (current_hour > sunset_hour) or (current_hour < sunrise_hour):
            print("              (nighttime at your location)")
            nightime_at_your_location = True
        else:
            nightime_at_your_location = False


        # Refresh sunrise / sunset times if needed to keep in sync
        if current_dt.date() == sunrise_dt.date():
            sunrise_dt, sunset_dt = get_todays_sunrise_sunsets()


        # Show current position of ISS relative to user
        iss_latitude, iss_longitude = get_iss_current_position()
        print(f"user position: lat={MY_LATITUDE} long={MY_LONGITUDE}")
        print(f"iss position: lat={iss_latitude} long={iss_longitude}")


        # The ISS is passing nearby: Send emails until out of range!!
        # if (abs(MY_LATITUDE - iss_latitude) <= 5) and (abs(MY_LONGITUDE - iss_longitude) <= 5):
        if 1 == 1:
            msg = EmailMessage()
            msg["Subject"] = "The ISS is passing nearby!"
            msg["From"] = SENDER_EMAIL
            msg["To"] = SENDER_EMAIL
            msg.set_content(f"Big news! The ISS is currently at latitude longitude coordinates: {iss_latitude},{iss_longitude}.\n\n This is very close to your coordinates of {MY_LATITUDE},{MY_LONGITUDE}.\n\nNotifications will continue, until the ISS is out of range...")

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


        # Pause execution for 60 seconds
        time.sleep(60) 
        
except KeyboardInterrupt:
    print("\n\nTimer stopped by user.")
