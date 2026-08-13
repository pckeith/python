#*****************************************************
# Rain Alert App:                                    *
# Author:    Keith Caldwell                          *
# Date:      August 11,2026                          *
#*****************************************************
# Description:                                       *
# This task is Day 35 of 100 days of Python:         *
# The purpose of this script is to use a defined     *
# API format and API key to call out to the          *
# openweathermap.org website, and pull weather data  *
# for a given geographic location.                   *
#                                                    *
# I used latitude and longitude coordinates for      *
# the latitude and longitude of my city, and also    *
# used my API key. here's the URL format:            *
# https://api.openweathermap.org/data/2.5/forecast?  *
# lat=(your lat)&lon={your lon}&appid={your app ID}  *
#                                                    *
# Running the URL in the above format will give you  *
# a series of 40 forecast for the next 5 days (in 3  *
# hour increments). There will be 40 occurances. But *
# if you look at the parameters, I added a count of  *
# just 4, using the "cnt" parameter - to look for    *
# rain only for the next 12 hours (3 hour increments *
# times 4 occurances, due to the count filter)       *
#                                                    *
# In addition to calling the Open Weather API, this  *
# program also uses Twilio to send SMS text messages *
# a phone, instead of printing a message or sending  *
# a message to email. You may recall (on an earlier  *
# day) we had implemented the Python smtplib to send *
# email: On this particular day, we're installing    *
# the twilio library and importing the twilio.rest   *
# Client to implement SMS texting.                   *
#                                                    *
# To run today's code (writing to SMS), you'll need  *
# to first install twilio, and then import the       *
# twilio rest Client. Because Twilio is a premium    *
# SaaS app vendor, you'd also need to setup a trial  *
# account with Twilio (substituting your trial       *
# account credentials in the code) in order to make  *
# this script work properly.                         * 
#                                                    *
# Caution:                                           *
# This script is technically correct for sending an  *
# SMS text message via Twilio. However, I discovered *
# if you're in the USA, there is a mountain of       *
# regulatory (not technical) hurdles to do this.     *
# The 4 steps Twilio will ask you to complete are    *
# as follows:                                        * 
#                                                    *
# 1) Set up a compliance profile                     *
# 2) Select a messaging service.                     *
# 3) Set up an A2P Brand registration.               *
# 4) Set up an A2P Campaign registration.            *
#                                                    *
# I spent all last night trying to going through     *
# these A2P brand and campaign registration steps,   *
# and could not get Twilio to accept my application, *
# although I provided answers to all their forms,    *
# multiple times. I discovered it's not easy to get  *
# permission from the US network of cellular         *
# providers, to send SMS messages on US networks!!   *
#                                                    *
# However, if you do want to experiment with this,   *
# and you attempted to send an SMS message which     *
# appeared to work (but was never received), you     *
# can use the other script I left in this directory  *
# named "check_twilio_sent_msg_status.py" to further *
# investigate details regarding what happened.       *
#*****************************************************
from pathlib import *
from twilio.rest import Client
import os
from dotenv import load_dotenv
import requests
import html
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

bring_umbrella = False

# ---------------------------- FUNCTION DEFINITIONS ------------------- #

def make_weather_request():

    #*****************************************************************
    # Parameters are shown below. Further documentation for Open     *
    # Trivia API can be found at:                                    *
    #                                                                *
    # https://openweathermap.org/api                                 *
    #*****************************************************************
    weather_app_id = os.getenv("WEATHER_APP_ID")
    parameters = {
        "lat": 44.8041,
        "lon": -93.1669,
        "cnt": 4,
        "appid": f"{weather_app_id}"
    }

    response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
    response.raise_for_status()
    data = response.json()
    # print(data)
    return data


# ---------------------------- MAIN PROGRAM FLOW ---------------------- #

#*********************************************************
# Note: Use Environment variables to keep confidential   *
#       information out of the Python program code. This *
#       way it's only loaded at runtime, when needed.    *
#*********************************************************
load_dotenv() # Get Weather & Twilio account information

data = make_weather_request()


# 1. Access top-level metadata fields
response_code = data['cod']
response_message = data['message']
item_count = data['cnt']

print("--- Top Level Metadata ---")
print(f"Response Code (cod): {response_code}")
print(f"Message: {response_message}")
print(f"Count of timestamps (cnt): {item_count}\n")


# 2. Access nested 'city' fields
city_dict = data['city']
city_id = city_dict['id']
city_name = city_dict['name']
city_country = city_dict['country']
city_population = city_dict['population']
city_timezone = city_dict['timezone']
city_sunrise = city_dict['sunrise']
city_sunset = city_dict['sunset']

# Double-nested coordinate fields inside city
city_lat = city_dict['coord']['lat']
city_lon = city_dict['coord']['lon']

print("--- City Information ---")
print(f"City ID: {city_id}")
print(f"City Name: {city_name}")
print(f"Coordinates: Lat {city_lat}, Lon {city_lon}")
print(f"Country: {city_country}")
print(f"Population: {city_population}")
print(f"Timezone Offset: {city_timezone}")
print(f"Sunrise (UX): {city_sunrise}")
print(f"Sunset (UX): {city_sunset}\n")


# 3. Access elements inside the 'list' array
forecast_list = data['list']

print("--- Iterating Through Forecast List ---")
for index, forecast in enumerate(forecast_list):
    # Each item in the list is a dictionary
    timestamp = forecast.get('dt')
    
    # Extract nested fields using .get() to prevent KeyErrors if data is missing
    main_data = forecast.get('main', {})
    temperature = main_data.get('temp')
    humidity = main_data.get('humidity')
    
    # Weather is usually a list containing a dictionary
    weather_list = forecast.get('weather', [])
    weather_condition = weather_list[0].get('main') if weather_list else "N/A"
    weather_id = weather_list[0].get('id') if weather_list else "N/A"
    weather_icon = weather_list[0].get('icon') if weather_list else "N/A"
    if weather_id < 700:
        bring_umbrella = True
    
    print(f"Index {index} | Time: {timestamp} | Temp: {temperature}K | Humidity: {humidity}% | Condition: {weather_condition} | Weather ID: {weather_id} | Weather Icon: {weather_icon}")


if bring_umbrella == True:
    print("\nBring an umbrella, precipitation is likely!!")
    print("\n")

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    sms_message_body="Bring an umbrella, precipitation is likely!!☔"
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone_nbr = os.getenv("TWILIO_PROVIDED_PHONE_NBR")
    dest_phone_nbr = os.getenv("TWILIO_DEST_PHONE_NBR")

    client = Client(account_sid, auth_token)
    try:
        # Send the message
        # Note: Phone numbers must be written in strict E.164 format (e.g., +1234567890)
        message = client.messages.create(
            body=f"{sms_message_body}",
            from_=f"{twilio_phone_nbr}",  # Replace with your provided Twilio phone number
            to=f"{dest_phone_nbr}"        # Replace with your personal verified phone number
        )
    
        # Confirm delivery status by printing the unique message SID
        print(f"Weather message sent successfully! SID: {message.sid}")

    except Exception as e:
        print(f"An error occurred: {e}")
