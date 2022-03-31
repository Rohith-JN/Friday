# Functions for Friday

import calendar
import datetime
import os
import subprocess
import webbrowser
import psutil
import requests
import yfinance
import re
import wolframalpha
import speech_recognition as sr
import pyttsx3
from paths import paths
from difflib import SequenceMatcher
from API_keys import *

engine = pyttsx3.init('sapi5')
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()
    

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


#getcurrent-day
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


#get-current-location
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
def getStock(search_term):
    global full_name, change_percent, change_no, state, price, currency
    results = []
    query = requests.get(f'https://yfapi.net/v6/finance/autocomplete?region=IN&lang=en&query={search_term}',
                         headers={
                             'accept': 'application/json',
                             'X-API-KEY': yfinance_api_key
                         })
    response = query.json()
    for i in response['ResultSet']['Result']:
        final = i['symbol']
        results.append(final)

    newQuery = requests.get(f'https://yfapi.net/v7/finance/options/{results[0]}',
                            headers={
                                'accept': 'application/json',
                                'X-API-KEY': yfinance_api_key
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


#function-to-get-quick-answers
def getQuickAnswers(query):
    url = "https://api.duckduckgo.com"
    response = requests.get(url, params={"q": query, "format": "json"})
    data = response.json()
    final = ' '.join(re.split(r'(?<=[.])\s', data['Abstract'])[:2])
    if final == '':
        appId = wolframalphaApIKey
        client = wolframalpha.Client(appId)
        res = client.query(query)
        answer = next(res.results).text
        return answer
    else:
        return final


#get-weather-of-current-location
def getWeather():
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


#greet-function
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning Boss"
    elif 12 <= hour < 18:
        return "Good Afternoon Boss"
    else:
        return "Good evening Boss"


#get-weather-of-location
def getWeatherLocation(search_term):
    api_key = OpenWeather_API_Key
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + search_term
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        weather_description = z[0]["description"]
        temperature = int(current_temperature - 273.15)
        return f"Current temperature in {search_term} is {temperature} degree celsius with {weather_description}"
    else:
        return "City Not Found"


#close-app
def close_app(app_name):
    running_apps=psutil.process_iter(['pid','name'])
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in app_name.split() or app_name in sys_app:
            pid=app.info.get('pid')
            
            try:
                app_pid = psutil.Process(pid)
                app_pid.terminate()
                found=True
            except: pass
            
        else: pass
    if not found:
        return app_name + " is not running"
    else:
        return 'Closed ' + app_name

#open-app
def checkIfProcessRunning(processName):
    running_apps=psutil.process_iter(['pid','name'])
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in processName.split() or processName in sys_app:
            pid=app.info.get('pid')
            
            try:
                found=True
            except: pass
            
        else: pass
    if not found:
        return False
    else:
        return True

def open_app(name):
    for app_name in paths:
        for app in app_name:
            s = SequenceMatcher(None, app, name)
            if s.ratio() > 0.6 and checkIfProcessRunning(app) == True:
                return speak(f'{name} is already running')
            
            elif s.ratio() > 0.6 and checkIfProcessRunning(app) == False:
                speak(f"Opening {app}")
                return os.startfile(paths.get(app_name))
            
    else:
        speak(f'You do not have an app named {name}')

#open-youtube
def openYoutube():
    speak("opening youtube")
    webbrowser.open_new_tab("https://www.youtube.com")

#get-current-location
def location():
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    state = data["region"].split(',')
    speak(f'You are in {city},{state}')
    print(f'You are in {city},{state}')
