import random
import re
import speech_recognition as sr
import pyttsx3
import datetime
import yfinance as yf
import pywhatkit as kit
import webbrowser
import psutil
import time
import subprocess
import screen_brightness_control as sbc
import pyjokes
import pyscreenshot
import calendar
from API_methods import *
from API_creds import *
import win10toast
import asyncio
import requests
import wolframalpha
import platform
import keyboard
import pyautogui


if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


current_brightness = sbc.get_brightness()
notification = win10toast.ToastNotifier()


def getDay():
    today = datetime.datetime.now()
    date = today.strftime("%d %m %y")
    day = datetime.datetime.strptime(date, '%d %m %y').weekday()
    return calendar.day_name[day]


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
    file_name = str(date).replace(':', '-') + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    sublime = 'C:\Program Files\Sublime Text\sublime_text.exe'
    subprocess.Popen([sublime, file_name])

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
        speak(f"Current temperature is {temperature} degree celsius with {weather_description}")
        print(f"Current temperature is {temperature} degree celsius with {weather_description}")
    else:
        speak("City Not Found")
        print("City Not Found")


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
        speak(
            f"Current temperature in {search_term} is {temperature} degree celsius with {weather_description}")
        print(
            f"Current temperature in {search_term} is {temperature} degree celsius with {weather_description}")
    else:
        speak("City Not Found")
        print("City not found")

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
        stock = yf.Ticker(results[0])
        price = stock.info["regularMarketPrice"]
        full_name = stock.info['longName']
        currency = stock.info["currency"]
    except Exception as e:
        print(e)

    return f"Shares of {full_name} {state} by {change_percent} percent or {change_no} at {price} {currency}"


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
        speak(app_name + " is not running")
    else:
        speak('Closed ' + app_name)


win10toast.ToastNotifier().show_toast("Friday", 'Friday has been started', duration=5)
wishMe()

async def main():
    
    def there_exists(terms):
        for term in terms:
            if term in response:
                return True

    WakeCommand = 'hello'

    while True:
        print("Listening..")
        response = takeCommand()

        if response.count(WakeCommand) > 0:
            speak("Yes boss")
            response = takeCommand()

            if "good bye" in response or "ok bye" in response or "stop" in response or "see you later" in response or "bye" in response or "kill program" in response or "sleep" in response:
                res = ['See you later', 'Good bye..', 'Nice talking with you', 'Bye..']
                speak(random.choice(res))
                break

            elif there_exists(['close']):
                search_term = response.replace('close', '')
                close_app(search_term)

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

            elif there_exists(["current location", "location", "where am i", "where am I right now"]):
                res = requests.get("https://ipinfo.io/")
                data = res.json()
                city = data["city"].split(',')
                state = data["region"].split(',')
                speak(f'You are in {city},{state}')
                print(f'You are in {city},{state}')

            elif there_exists(['increase volume', 'volume up']):
                for i in range(3):
                    pyautogui.press('volumeup')

            elif there_exists(['decrease volume', 'volume down']):
                for i in range(3):
                    pyautogui.press('volumedown')

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
                engine.setProperty("rate", 150)
                search_term = response.lower().split(" of ")[-1].strip()
                stock = getStock(search_term)
                speak(stock)
                print(stock)
                engine.setProperty("rate", 175)

            elif there_exists(['take a note', 'note', 'note this down', 'remember this', 'take this down']):
                speak("What do you want me to note down?")
                response = takeCommand()
                note(response)
                speak("I have made a note of that")

            elif "open vscode" in response or "open visual studio code" in response:
                speak("opening visual studio code")
                subprocess.call(
                    "C://Users//ACERq//AppData//Local//Programs//Microsoft VS Code//Code.exe")

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

            elif there_exists(["close current tab", 'close tab']):
                keyboard.press_and_release('ctrl+w') 

            elif 'time' in response or "what is the time" in response or "what's the time" in response:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"the time is {strTime}")

            elif "open stackoverflow" in response or "stack overflow" in response:
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

            elif there_exists(['what is the weather like right now', 'current temperature', 'climate']):
                getWeather()

            elif there_exists(['increase brightness']):
                brightness = sbc.set_brightness(current_brightness + 10)
                speak(f"Increased brightness by 10 percent")

            elif there_exists(
                    ['decrease brightness', 'dim', 'dim the laptop', 'dim the screen', 'the screen is too bright']):
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

            elif there_exists(['what is the weather in']):
                search_term = response.replace("what is the weather in", '')
                getWeatherLocation(search_term)

            elif there_exists(['open android studio']):
                speak("Opening android studio")
                subprocess.call(
                    "C://Program Files//Android//Android Studio//bin//studio64.exe")

            elif there_exists(['open telegram']):
                speak("Opening telegram")
                subprocess.call(
                    "C://Users//ACERq//AppData//Roaming//Telegram Desktop//Telegram.exe")

            elif there_exists(['open discord']):
                speak("Opening discord")
                subprocess.call(
                    "C://Users//ACERq//AppData//Local//Discord//Update.exe")

            elif there_exists(['send a message to']):
                search_term = response.replace('send a message to', '').lower()

                if there_exists(['SD dudes', 'sd', 'sd dudes']):
                    speak("What should I send")
                    response = takeCommand()
                    await Methods().sendGroupMessage(CHAT_ID_1, response)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to SD dudes in Telegram", duration=10)

                elif there_exists(['Epic group', 'epic', 'epic dudes']):
                    speak("What should I send")
                    response = takeCommand()
                    await Methods().sendGroupMessage(CHAT_ID_2, response)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to Epic dudes in Telegram", duration=10)

                elif there_exists(['arun', 'Arun']):
                    speak("What should I send?")
                    response = takeCommand()
                    await Methods().sendPersonalMessage(response, user_id_2)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to Arun in Telegram", duration=10)

                elif there_exists(['pranav', 'Pranav']):
                    speak("What should I send?")
                    response = takeCommand()
                    await Methods().sendPersonalMessage(response, user_id_1)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to Pranav in Telegram", duration=10)

                elif there_exists(['thomas', 'Thomas']):
                    speak("What should I send?")
                    response = takeCommand()
                    await Methods().sendPersonalMessage(response, user_id_3)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to Thomas in Telegram", duration=10)

                elif there_exists(['mom', 'Rajath', 'Rajat', 'rajat', 'mum']):
                    speak("What should I send?")
                    response = takeCommand()
                    await Methods().sendPersonalMessage(response, user_id_4)
                    speak("Message sent successfully")
                    print("Message sent successfully")
                    notification.show_toast("Friday", "Sent a message to Rajath in Telegram", duration=10)

            elif there_exists(['open github desktop', 'github desktop']):
                speak("Opening Github desktop")
                subprocess.call('C://Users//ACERq//AppData//Local//GitHubDesktop//GithubDesktop.exe')

            elif there_exists(['open brave', 'brave']):
                speak("Opening brave")
                subprocess.call('C://Program Files//BraveSoftware//Brave-Browser//Application//brave.exe')

            elif there_exists(['open postman', 'open Postman']):
                speak("Opening Postman")
                subprocess.call('C://Users//ACERq//AppData//Local//Postman//Postman.exe')

            elif there_exists(['open youtube music', 'open Youtube Music']):
                speak("Opening Youtube Music")
                subprocess.call('C://Program Files//Google//Chrome//Application//chrome_proxy.exe')

            elif there_exists(['what', 'who', 'why', 'where', 'when', 'which']):
                ans = getQuickAnswers(response)
                speak(ans)
                print(ans)

asyncio.run(main())
time.sleep(3)