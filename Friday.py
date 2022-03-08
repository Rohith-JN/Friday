import json
import random
import datetime
import sys
import pywhatkit as kit
import webbrowser
import psutil
import time
import subprocess
import screen_brightness_control as sbc
import pyjokes
import pyscreenshot
import win10toast
import asyncio
import platform
import keyboard
import pyautogui
from Friday_Functions import *
from API_methods import *
from API_creds import *
import torch
from Model import NeuralNet
from NLTK import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


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

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

async def main():
    
    def there_exists(terms):
        for term in terms:
            if term in response:
                return True

    WakeCommands = ['wake up', 'hey friday', 'Hey Friday', 'hey Friday', 'hello', 'Friday', 'friday']

    while True:
        print("Listening..")
        response = takeCommand()
        
        for wakeCommand in WakeCommands:
            if response.count(wakeCommand) > 0:
                speak("Yes boss")
                response = takeCommand()

                sentence = tokenize(response)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)

                tag = tags[predicted.item()]

                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]

                if prob.item() > 0.75:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            speak(f"{random.choice(intent['responses'])}")
                else:
                    pass

                if there_exists(["close current tab", 'close tab']):
                    keyboard.press_and_release('ctrl+w') 

                elif there_exists(['goodbye', 'bye', 'see you later', 'ok bye']):
                    speak("Nice talking with you!")
                    sys.exit(0)

                elif there_exists(['close']):
                    search_term = response.replace('close', '')
                    status = close_app(search_term)
                    speak(status)

                elif there_exists(['open google', 'open new tab in google', 'new tab in google']):
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("Google chrome is open now")
                    time.sleep(5)

                elif there_exists(['open gmail', 'gmail']):
                    speak("opening gmail")
                    webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
                    speak("Gmail is open now")
                    time.sleep(5)

                elif there_exists(['open']):
                    search_term = response.replace('open', '')
                    search_term = "".join(search_term.split())
                    open_app(search_term)

                elif there_exists(['whats the day today', 'what day is it today', 'day']):
                    speak(f'Today is {getDay()}')

                elif 'open youtube' in response:
                    openYoutube()

                elif there_exists(['battery percentage', 'what is the battery like right now', 'tell me the battery percentage']):
                    speak("Current battery percentage is at" + str(percent) + "percent")

                elif there_exists(['what is the current brightness', 'current brightness', 'what is the brightness like right now']):
                    speak(str(sbc.get_brightness()) + "percent")

                elif there_exists(["current location", "location", "where am i", "where am I right now"]):
                    location()

                elif there_exists(['increase volume', 'volume up']):
                    for i in range(3):
                        pyautogui.press('volumeup')
                    speak("Increase volume by 10 percent")

                elif there_exists(['decrease volume', 'volume down']):
                    for i in range(3):
                        pyautogui.press('volumedown')
                    speak("Decreased volume by 10 percent")

                elif there_exists(["play"]):
                    search_term = response.replace("play", '')
                    kit.playonyt(search_term)
                    speak(f"Playing {search_term}")

                elif there_exists(["on youtube"]):
                    search_term = response.replace("on youtube", '')
                    url = f"https://www.youtube.com/results?search_query={search_term}"
                    webbrowser.get().open(url)
                    speak(f'Here is what I found for {search_term} on youtube')

                elif there_exists(["price of", "what is the price of", "tell me the price of"]):
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

                elif there_exists(['tell me a joke', 'not funny', 'make me laugh', 'joke', 'tell me another joke']):
                    joke = (pyjokes.get_joke())
                    speak(joke)
                    print(joke)

                elif there_exists(["search for"]) and 'youtube' not in response:
                    search_term = response.split("for")[-1]
                    url = f"https://google.com/search?q={search_term}"
                    webbrowser.get().open(url)
                    speak(f'Here is what I found for {search_term} on google')

                elif there_exists(['what is the time now', 'what time is it', 'time']):
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(f"the time is {strTime}")

                elif 'search' in response:
                    response = response.replace("search", "")
                    webbrowser.open_new_tab(response)
                    time.sleep(5)

                elif there_exists(['sign out', 'log off']):
                    speak(
                        "Your pc will log off in 10 sec make sure you exit from all applications")
                    subprocess.call(["shutdown", "/l"])

                elif there_exists(['shutdown the pc', 'shutdown', 'shutdown the laptop']):
                    speak("Shutting down your pc, make sure you exit from all applications")
                    subprocess.call(["shutdown", "/s"])

                elif there_exists(['restart', 'restart the pc', 'restart the laptop']):
                    speak("Restarting your pc, make sure you exit from all applications")
                    subprocess.call(["shutdown", "/r"])

                elif there_exists(['what is the weather like right now', 'current temperature', 'climate']):
                    weather = getWeather()
                    speak(weather)
                    print(weather)

                elif there_exists(['increase brightness', 'the brightness is low']):
                    if sbc.get_brightness() == 100:
                        speak("Brightness is already at max")
                    else:
                        brightness = sbc.set_brightness(current_brightness + 10)
                        speak(f"Increased brightness by 10 percent")

                elif there_exists(
                        ['decrease brightness', 'dim', 'dim the laptop', 'dim the screen', 'the screen is too bright']):
                    brightness = sbc.set_brightness(current_brightness - 10)
                    speak(f"Decreased brightness by 10 percent")

                elif there_exists(['take a screenshot', 'screenshot', 'capture the screen', 'take a photo of this']):
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

                elif there_exists(['what', 'who', 'why', 'where', 'when', 'which']):
                    ans = getQuickAnswers(response)
                    speak(ans)
                    print(ans)

                '''
                elif there_exists(['send a message to']):
                    search_term = response.replace('send a message to', '').replace(' ', '')
                    await sendUserMessage(search_term)
                '''

asyncio.run(main())
time.sleep(3)

