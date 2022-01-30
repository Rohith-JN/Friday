import math
import random
import speech_recognition as sr
import pyttsx3
import datetime
import yfinance as yf
import pywhatkit as kit
import webbrowser
import psutil
import os
import time
import subprocess
import screen_brightness_control as sbc
import pyjokes
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def there_exists(terms):
    for term in terms:
        if term in response:
            return True


engine = pyttsx3.init('sapi5')
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# battery module commands
battery = psutil.sensors_battery()
percent = battery.percent


def speak(text):
    engine.say(text)
    engine.runAndWait()

def getLocation():
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    state = data["region"].split(',')
    return city


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Boss")
        print("Good Morning Boss")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss")
        print("Good Afternoon Boss")
    else:
        speak("Good evening Boss")
        print("Good evening Boss")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            response = r.recognize_google(audio, language='en-in')
            print(f"user said:{response}\n")

        except Exception as e:
            return "None"
        return response.lower()


wake = "hello"

while True:
    print("Listening..")
    response = takeCommand()

    if response.count(wake) > 0:
        speak("Yes boss")
        response = takeCommand()

        if "good bye" in response or "ok bye" in response or "stop" in response or "see you later" in response or "bye" in response or "kill program" in response or "sleep" in response:
            res = ['See you later', 'Good bye..', 'Nice talking with you', 'Bye..']
            speak(random.choice(res))
            break

        if "how are you" in response or "how are you doing" in response:
            speak("I'm very well, thanks for asking")

        elif 'open youtube' in response:
            speak("opening youtube")
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(4)

        elif "battery percentage" in response or "battery" in response or "what is the battery percentage" in response:
            speak("Current battery percentage is at" + str(percent) + "percent")

        elif "notepad" in response or "open notepad" in response:
            subprocess.call("C://Windows//System32//notepad.exe")
            speak("opened notepad")

        elif "current brightness" in response or "what is the current brightness" in response:
            speak(str(sbc.get_brightness()) + "percent")

        elif there_exists(["current location","location","where am i","where am i right now"]):
            res = requests.get("https://ipinfo.io/")
            data = res.json()
            city = data["city"].split(',')
            state = data["region"].split(',')
            speak(f'You are in {city},{state}')
            print(f'You are in {city},{state}')
            
        elif there_exists(["play"]):
            search_term = response.replace("play", '')
            kit.playonyt(search_term)
            speak(f"Playing {search_term}")

        elif there_exists(["on youtube"]):
            search_term = response.replace("on youtube", '')
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on youtube')

        elif there_exists(["price of"]):
            # strip removes whitespace after/before a term in string
            search_term = response.lower().split(" of ")[-1].strip()
            stocks = {
                "apple": "AAPL",
                "microsoft": "MSFT",
                "facebook": "FB",
                "tesla": "TSLA",
                "bitcoin": "BTC-USD"
            }
            try:
                stock = stocks[search_term]
                stock = yf.Ticker(stock)
                price = stock.info["regularMarketPrice"]

                speak(
                    f'price of {search_term} is {price} {stock.info["currency"]}')
            except:
                speak('oops, something went wrong')

        elif "open vscode" in response or "open visual studio code" in response:
            speak("opening visual studio code")
            subprocess.call(
                "C://Users//Rohith JN//AppData//Local//Programs//Microsoft VS Code//Code.exe")

        elif "close vscode" in response or "close visual studio code" in response:
            speak("closing visual studio code")
            os.system("taskkill /f /im code.exe")

        elif "tell me a joke" in response or "joke" in response:
            joke = (pyjokes.get_joke())
            speak(joke)
            print(joke)

        elif 'open google' in response:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in response:
            speak("opening gmail")
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
            speak("Gmail is open now")
            time.sleep(5)

        elif "open a new tab in google" in response or "open new tab" in response:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opened new tab")

        elif there_exists(["search for"]) and 'youtube' not in response:
            search_term = response.split("for")[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on google')

        elif "close google" in response or "shutdown google" in response:
            os.system("taskkill /f /im chrome.exe")

        elif 'time' in response or "what is the time" in response or "what's the time" in response:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in response or 'what can you do' in response:
            speak('I am Friday your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather'
                  'in different cities , get top headline news and you can ask me computational or geographical questions too!')

        elif "open stackoverflow" in response:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif "calculator" in response:
            subprocess.call("calc.exe")

        elif 'search' in response:
            response = response.replace("search", "")
            webbrowser.open_new_tab(response)
            time.sleep(5)

        elif "log off" in response or "sign out" in response or "kill switch" in response:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "shutdown" in response:
            speak("Shutting down your pc, make sure you exit from all applications")
            subprocess.call(["shutdown", "/s"])

        elif "restart" in response:
            speak("Restarting laptop, make sure you exit from all applications")
            subprocess.call(["shutdown", "/r"])

        elif there_exists(['weather', 'whats the weather like right now', 'current termperature', 'climate']):
            api_key=API_KEY
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            complete_url=base_url+"appid="+api_key+"&q="+"Bangalore"
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                temperature = int(current_temperature - 273.15)
                speak(f"Current temperature is {temperature} degree celsius with {weather_description}")
            else:
                speak(" City Not Found ")

time.sleep(3)
