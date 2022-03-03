import random
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
from API_methods import *
from API_creds import *
import win10toast
import asyncio
import requests
import platform
import keyboard
import pyautogui
from Friday_Functions import *


if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


current_brightness = sbc.get_brightness()
notification = win10toast.ToastNotifier()


# battery module commands
battery = psutil.sensors_battery()
percent = battery.percent


win10toast.ToastNotifier().show_toast("Friday", 'Friday has been started', duration=5)
speak(wishMe())
print(wishMe())

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
                status = close_app(search_term)
                speak(status)

            elif there_exists(['whats the day today', 'what day is it today', 'day']):
                speak(f'Today is {getDay()}')

            elif "how are you" in response or "how are you doing" in response:
                speak("I'm very well, thanks for asking")

            elif 'open youtube' in response:
                openYoutube()

            elif "battery percentage" in response or "battery" in response or "what is the battery percentage" in response:
                speak("Current battery percentage is at" + str(percent) + "percent")

            elif "current brightness" in response or "what is the current brightness" in response:
                speak(str(sbc.get_brightness()) + "percent")

            elif there_exists(["current location", "location", "where am i", "where am I right now"]):
                location()

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
                weather = getWeather()
                speak(weather)
                print(weather)

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
                weather = getWeatherLocation(search_term)
                speak(weather)
                print(weather)

            elif there_exists(['send a message to']):
                search_term = response.replace('send a message to', '').lower()

                if there_exists(['SD dudes', 'sd', 'sd dudes']):
                    await sendGroupMessage(CHAT_ID_1, 'SD Dudes')

                elif there_exists(['Epic group', 'epic', 'epic dudes']):
                    await sendGroupMessage(CHAT_ID_2, 'Epic Dudes')

                elif there_exists(['arun', 'Arun']):
                    await sendUserMessage(user_id_2, 'Arun')

                elif there_exists(['pranav', 'Pranav']):
                    await sendUserMessage(user_id_1, 'Pranav')

                elif there_exists(['thomas', 'Thomas']):
                    await sendUserMessage(user_id_3, 'Thomas')

                elif there_exists(['mom', 'Rajath', 'Rajat', 'rajat', 'mum']):
                    await sendUserMessage(user_id_4, 'Rajath')

            elif there_exists(['what', 'who', 'why', 'where', 'when', 'which']):
                ans = getQuickAnswers(response)
                speak(ans)
                print(ans)

asyncio.run(main())
time.sleep(3)

