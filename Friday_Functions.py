# Functions for Friday
import calendar
import datetime
import os
import sys
import subprocess
import webbrowser
import psutil
import requests
import yfinance
import re
import wolframalpha
import speech_recognition as sr
import pyttsx3
from difflib import SequenceMatcher
from API import *

#PYTTSX3: python-text-to-speech
engine = pyttsx3.init('sapi5')
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
#takes voice input from user    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        sr.Recognizer().adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        audio = r.listen(source)

        try:
            response = r.recognize_google(audio, language='en-in')
            print(f"user said:{response}\n")

        except Exception as e:
            return "None"
        return response.lower()

#stops the program
def powerdown():
    speak("Nice talking with you")
    sys.exit(0)

#opens a new chrome tab
def google():
    webbrowser.open_new_tab("https://www.google.com")
    time.sleep(5)

#opens gmail in a new tab
def gmail():
    webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(5)

#raises volume if param status is up and decreases volume if status is down
def volume(status):
    if status == 'up':
        for i in range(3):
            pyautogui.press('volumeup')
            speak("Increased volume by 10 percent")
    elif status == 'down':
        for i in range(3):
            pyautogui.press('volumedown')
            speak("Decreased volume by 10 percent")

#notes down input from the user in a text file    
def notedown():
    speak("What do you want me to note down?")
    response = takeCommand()
    note(response)
    speak("I have made a note of that")

#tells a joke
def joke():
    joke = (pyjokes.get_joke())
    speak(joke)

#logs-off the pc
def logoff():
    speak(
        "Your pc will log off in 10 sec make sure you exit from all applications")
    subprocess.call(["shutdown", "/l"])
        
#shutsdown the pc        
def shutdown():
    speak("Shutting down your pc, make sure you exit from all applications")
    subprocess.call(["shutdown", "/s"])

#restarts the pc
def restart():
    speak("Restarting your pc, make sure you exit from all applications")
    subprocess.call(["shutdown", "/r"])

#changes brightness based on the param status
def brightness(status):
    if status == 'increase':
        if sbc.get_brightness() == 100:
            speak("Brightness is already at max")
        else:
            brightness = sbc.set_brightness(current_brightness + 10)
            speak(f"Increased brightness by 10 percent")
    elif status == 'decrease':
        if sbc.get_brightness() == 0:
            speak("Brightness is already at 0")
        else:
            sbc.set_brightness(current_brightness - 10)
            speak(f"Decreased brightness by 10 percent") 

#takes a screenshot and saves it
def screenshot():
    image = pyscreenshot.grab()
    speak("Should I open the image?")
    response = takeCommand()
    if there_exists(['yes', 'show', 'show the screenshot']):
        image.show()
    else:
        speak("Ok")

#gets the current day
def getDay():
    today = datetime.datetime.now()
    date = today.strftime("%d %m %y")
    day = datetime.datetime.strptime(date, '%d %m %y').weekday()
    return calendar.day_name[day]

#convert-list-to-string
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

#gets the current location
def getLocation():
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    return listToString(city)

#function-to-make-a-note
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(':', '-') + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    sublime = paths.get(sublime)
    subprocess.Popen([sublime, file_name])

#function-to-get-stocks
#requires yahoo finance api key
def getStock(search_term):
    try: 
        global full_name, change_percent, change_no, state, price, currency
        results = []
        query = requests.get(f'https://yfapi.net/v6/finance/autocomplete?region=IN&lang=en&query={search_term}',
                            headers={
                                'accept': 'application/json',
                                'X-API-KEY': yfinance_API_key
                            })
        response = query.json()
        for i in response['ResultSet']['Result']:
            final = i['symbol']
            results.append(final)

        newQuery = requests.get(f'https://yfapi.net/v7/finance/options/{results[0]}',
                                headers={
                                    'accept': 'application/json',
                                    'X-API-KEY': yfinance_API_key
                                })
        response = newQuery.json()
        for i in response['optionChain']['result']:
            change_percent = i['quote']['regularMarketChangePercent']
            change_no = i['quote']['regularMarketChange']
            if '-' in str(change_percent):
                state = 'fell'
            else:
                state =  'rose'
    
            change_percent = round(change_percent, 2)
            change_no = round(change_no, 2)

        try:
            stock = yfinance.Ticker(results[0])
            price = stock.info["regularMarketPrice"]
            full_name = stock.info['longName']
            currency = stock.info["currency"]
        except Exception as e:
            print(e)

        return f"Shares of {full_name} {state} by {change_percent} percent or {change_no} at {price} {currency}"
        
    except Exception as e:
        speak(e)

#function-to-get-quick-answers from duckduckgo
def getQuickAnswers(query):
    try:
        url = "https://api.duckduckgo.com"
        response = requests.get(url, params={"q": query, "format": "json"})
        data = response.json()
        final = ' '.join(re.split(r'(?<=[.])\s', data['Abstract'])[:2])
        if final == '':
            appId = wolframalpha_API_Key
            client = wolframalpha.Client(appId)
            res = client.query(query)
            answer = next(res.results).text
            return answer
        else:
            return final
    except Exception as e:
        speak(e)

#get-weather-of-current-location
#requires open weather api key
def getWeather():
    try:
        api_key = OpenWeather_API_Key
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + getLocation()
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]
            temperature = int(current_temperature - 273.15)

            return f"Current temperature is {temperature} degree celsius with {weather_description}"
        else:
            return "City Not Found"
    except Exception as e:
        speak(e)

def getWeatherLocation(location):
    try:
        api_key = OpenWeather_API_Key
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + location
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]
            temperature = int(current_temperature - 273.15)

            return f"Current temperature is {temperature} degree celsius with {weather_description}"
        else:
            return "City Not Found"
    except Exception as e:
        speak(e)

#greets the user
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning Boss"
    elif 12 <= hour < 18:
        return "Good Afternoon Boss"
    else:
        return "Good evening Boss"

#opens youtube in a new tab
def openYoutube():
    speak("opening youtube")
    webbrowser.open_new_tab("https://www.youtube.com")

#gets the current location
def location():
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    state = data["region"].split(',')
    speak(f'You are in {city},{state}')
    print(f'You are in {city},{state}')
