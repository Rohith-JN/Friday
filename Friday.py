import pywhatkit as kit
import webbrowser
import screen_brightness_control as sbc
import asyncio
import platform
import keyboard
from Friday_Functions import *
from Telethon_methods import *
from typing import Hashable
from API_keys import *
from dataclasses import dataclass

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

speak(wishMe())

current_brightness = sbc.get_brightness()
battery = psutil.sensors_battery()
percent = battery.percent

@dataclass
class ActionInput(Hashable):
    def __hash__(self) -> int:
        return str(self.value).__hash__()

    value: list[str]

async def main():

    def there_exists(terms):
        for term in terms:
            if term in response or SequenceMatcher(None, response, term).ratio() > 0.85:
                return True

    while True:
        print("Listening..")
        response = takeCommand()

        def youtube():
            search_term = response.replace("play", '')
            kit.playonyt(search_term)
            speak(f"Playing {search_term}")

        def searchYoutube():
            search_term = response.replace("on youtube", '')
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on youtube')

        def stock():
            engine.setProperty("rate", 150)
            search_term = response.lower().split(" of ")[-1].strip()
            stock = getStock(search_term)
            speak(stock)
            print(stock)
            engine.setProperty("rate", 175)

        def search():
            search_term = response.split("for")[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on google')

        def weather():
            search_term = response.replace("what is the weather in", '')
            weather = getWeatherLocation(search_term)
            speak(weather)
            print(weather)
            
        actions = {
            ActionInput(["close current tab", 'close tab']): (lambda: keyboard.press_and_release('ctrl+w')),
            ActionInput(['goodbye', 'bye', 'see you later', 'ok bye']): (lambda: powerdown()),
            ActionInput(['open google', 'open new tab in google', 'new tab in google']): (lambda: google()),
            ActionInput(['gmail', 'open gmail']): (lambda: gmail()),
            ActionInput(['open youtube']): (lambda: openYoutube()),
            ActionInput(['whats the day today', 'what day is it today', 'day']): (lambda: speak(f'Today is {getDay()}')),
            ActionInput(['battery percentage', 'what is the battery like right now', 'tell me the battery percentage']): (lambda: speak("Current battery percentage is at" + str(percent) + "percent")),
            ActionInput(['what is the current brightness', 'current brightness', 'what is the brightness like right now']): (lambda: speak(str(sbc.get_brightness()) + "percent")),
            ActionInput(["current location", "location", "where am i", "where am I right now"]): (lambda: location()),
            ActionInput(['increase volume', 'volume up']): (lambda: volume('up')),
            ActionInput(['decrease volume', 'volume down']): (lambda: volume('down')),
            ActionInput(['play']): (lambda: youtube()),
            ActionInput(["on youtube"]): (lambda: searchYoutube()),
            ActionInput(["price of", "what is the price of", "tell me the price of"]): (lambda: stock()),
            ActionInput(['take a note', 'note', 'note this down', 'remember this', 'take this down']): (lambda: notedown()),
            ActionInput(['tell me a joke', 'not funny', 'make me laugh', 'joke', 'tell me another joke']): (lambda: joke()),
            ActionInput(['search for']): (lambda: search()),
            ActionInput(['what is the time now', 'what time is it', 'time']): (lambda: speak(f"the time is {datetime.datetime.now().strftime('%H:%M')}")),
            ActionInput(['sign out', 'log off']): (lambda: logoff()),
            ActionInput(['shutdown the pc', 'shutdown', 'shutdown the laptop']): (lambda: shutdown()),
            ActionInput(['restart', 'restart the pc', 'restart the laptop']): (lambda: restart()),
            ActionInput(['what is the weather like right now', 'current temperature', 'climate']): (lambda: speak(getWeather())),
            ActionInput(['increase brightness', 'the brightness is low']): (lambda: brightness('increase')),
            ActionInput(['decrease brightness', 'dim', 'dim the laptop', 'dim the screen', 'the screen is too bright']): (lambda: brightness('decrease')),
            ActionInput(['take a screenshot', 'screenshot', 'capture the screen', 'take a photo of this']): (lambda: screenshot()),
            ActionInput(['what is the weather in']): (lambda: weather()),
            ActionInput(['what', 'who', 'why', 'where', 'when', 'which']): (lambda: speak(getQuickAnswers((response)))),
        }

        for key in actions:
            if there_exists(key.value):
                actions[key]()

        if there_exists(['send a message to']):
            search_term = response.replace('send a message to', '').replace(' ', '')
            await Methods().sendUserMessage(search_term)

asyncio.run(main())
time.sleep(3)

