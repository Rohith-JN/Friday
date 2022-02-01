from http import client
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
import pyscreenshot
import calendar
from dotenv import load_dotenv
from spotifyClient import *

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHAT_ID_1 = os.getenv("CHAT_ID_1")
CHAT_ID_2 = os.getenv("CHAT_ID_2")
current_brightness = sbc.get_brightness()


def getDay():
    today = datetime.datetime.now()
    date = today.strftime("%d %m %y")
    day = datetime.datetime.strptime(date, '%d %m %y').weekday()
    return (calendar.day_name[day])


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


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def speak(text):
    engine.say(text)
    engine.runAndWait()

def getLocation():
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    return listToString(city)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(':','-') + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    sublime = 'C:\Program Files\Sublime Text\sublime_text.exe'
    subprocess.Popen([sublime, file_name])


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

def sendMessage(text, chat_id):
    base_url = "https://api.telegram.org/bot5272158533:AAHheD5P17Oyr4eHv3RdRZYF-5m9oP1bkxY/sendMessage"
    parameters = {
        "chat_id" : chat_id,
        "text" : text
    }
    res = requests.get(base_url, data = parameters)

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

        elif there_exists(['whats the day today', 'what day is it today', 'day']):
            speak(f'Today is {getDay()}')     

        elif "how are you" in response or "how are you doing" in response:
            speak("I'm very well, thanks for asking")

        elif 'open youtube' in response:
            speak("opening youtube")
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(4)

        elif "battery percentage" in response or "battery" in response or "what is the battery percentage" in response:
            speak("Current battery percentage is at" + str(percent) + "percent")

        elif "current brightness" in response or "what is the current brightness" in response:
            speak(str(sbc.get_brightness()) + "percent")

        elif there_exists(["current location", "location", "where am i", "where am i right now"]):
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
            search_term = response.lower().split(" of ")[-1].strip()
            stocks = {
                "apple": "AAPL",
                "microsoft": "MSFT",
                "facebook": "FB",
                "tesla": "TSLA",
                "bitcoin": "BTC-USD",
                "meta": "FB",
                "netflix": "NFLX",
                "nvidia": "NVDA",
                "intel": "INTC",
                "Tata Power": "TATAPOWER"
            }
            try:
                stock = stocks[search_term]
                stock = yf.Ticker(stock)
                price = stock.info["regularMarketPrice"]

                speak(
                    f'price of {search_term} is {price} {stock.info["currency"]}')
            except:
                speak('something went wrong')

        elif there_exists(['take a note', 'note', 'note this down', 'remember this', 'take this down']):
            speak("What do you want me to note down?")
            response = takeCommand()
            note(response)
            speak("I have made a note of that")

        elif "open vscode" in response or "open visual studio code" in response:
            speak("opening visual studio code")
            subprocess.call(
                "C://Users//ACERq//AppData//Local//Programs//Microsoft VS Code//Code.exe")

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
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"the time is {strTime}")

        elif 'who are you' in response or 'what can you do' in response:
            speak('I am Friday your personal assistant. I am programmed to minor tasks like'
                  'opening youtube, google chrome, gmail, predict time, take screenshots,'
                  'search google chrome, predict weather etc')

        elif "open stackoverflow" in response:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif "calculator" in response or 'calc' in response:
            subprocess.call("calc.exe")

        elif 'search' in response:
            response = response.replace("search", "")
            webbrowser.open_new_tab(response)
            time.sleep(5)

        elif "log off" in response or "sign out" in response or "kill switch" in response:
            speak(
                "Your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "shutdown" in response:
            speak("Shutting down your pc, make sure you exit from all applications")
            subprocess.call(["shutdown", "/s"])

        elif "restart" in response:
            speak("Restarting your pc, make sure you exit from all applications")
            subprocess.call(["shutdown", "/r"])

        elif there_exists(['weather', 'whats the weather like right now', 'current temperature', 'climate']):
            api_key = API_KEY
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url+"appid="+api_key+"&q="+getLocation()
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                z = x["weather"]
                weather_description = z[0]["description"]
                temperature = int(current_temperature - 273.15)
                speak(f"Current temperature is {temperature} degree celsius with {weather_description}")
            else:
                speak(" City Not Found ")
        
        elif there_exists(['increase brightness']):
            brightness = sbc.set_brightness(current_brightness + 10)
            speak(f"Increased brightness by 10 percent")

        elif there_exists(['decrease brightness']):
            brightness = sbc.set_brightness(current_brightness - 10)
            speak(f"Decreased brightness by 10 percent")

        elif "take a screenshot" in response or "screen shot" in response:
            image = pyscreenshot.grab()
            speak("Should I open the image?")
            response = takeCommand()
            if there_exists(['yes', 'show', 'show the screenshot']):
                image.show()
            else:
                speak("Ok boss")
        
        elif there_exists(['open android studio']):
            speak("Opening android studio")
            subprocess.call(
                "C://Program Files//Android//Android Studio//bin//studio64.exe")

        elif there_exists(['close android studio']):
            speak('Closing android studio')
            os.system("taskkill /f /im studio64.exe")

        elif there_exists(['open telegram']):
            speak("Opening telegram")
            subprocess.call(
                "C://Users//ACERq//AppData//Roaming//Telegram Desktop//Telegram.exe")

        elif there_exists(['close telegram']):
            speak('Closing telegram')
            os.system("taskkill /f /im Telegram.exe")

        elif there_exists(['open discord']):
            speak("Opening discord")
            subprocess.call(
                "C://Users//ACERq//AppData//Local//Discord//Update.exe")

        elif there_exists(['close discord']):
            speak('Closing discord')
            os.system("taskkill /f /im Update.exe")

        elif there_exists(['send a message in telegram', 'send a message']):
            speak("To which group should I send the message to?")
            response = takeCommand()
            if there_exists(['locality group']):
                speak("What should I send?")
                response = takeCommand()
                sendMessage(response, CHAT_ID_1)
                speak("Message sent successfully")
            elif there_exists(['class group', 'epic dudes']):
                speak("What should I send?")
                response = takeCommand()
                sendMessage(response, CHAT_ID_2)
                speak("Message sent successfully")

        elif there_exists(['open github desktop', 'github desktop']):
            speak("Opening Github desktop")
            subprocess.call('C://Users//ACERq//AppData//Local//GitHubDesktop//GithubDesktop.exe')

        elif there_exists(['close github', 'close github desktop']):
            speak("Closing Github desktop")
            os.system('taskkill /f /im GithubDesktop.exe')

        elif there_exists(['open brave', 'brave']):
            speak("Opening brave")
            subprocess.call('C://Program Files//BraveSoftware//Brave-Browser//Application//brave.exe')

        elif there_exists(['close brave', 'close brave']):
            speak("Closing brave")
            os.system('taskkill /f /im brave.exe')
            
time.sleep(3)