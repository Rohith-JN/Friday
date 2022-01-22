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


def there_exists(terms):
    for term in terms:
        if term in statement:
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


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss")
        print("Good Morning Boss")
    elif hour >= 12 and hour < 18:
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
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


speak("Your personal assistant, Friday is booting up now")
wishMe()
speak("what can I do for you")


if __name__ == '__main__':

    while True:
        statement = takeCommand().lower()
        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement or "see you later" in statement or "bye" in statement or "kill program" in statement or "sleep" in statement:
            speak('Friday is shutting down now, Goodbye boss')
            print('Friday is shutting down now, Goodbye boss')
            break

        if "how are you" in statement or "how are you doing" in statement:
            speak("I'm very well, thanks for asking")

        elif 'open youtube' in statement:
            speak("opening youtube")
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(4)

        elif there_exists(["terminate"]):
            search_term = statement.split("terminate" "")[1]
            os.system(f"taskkill /f /im {search_term}.exe")
            speak(f" closed {search_term}")

        elif "battery percentage" in statement or "battery" in statement or "what is the battery percentage" in statement:
            speak("Current battery percentage is at" + str(percent) + "percent")

        elif "close sublime text editor" in statement or "close sublime text 3" in statement or "close sublime" in statement:
            os.system("taskkill /f /im sublime_text.exe")
            speak("closed sublime text editor")

        elif "close spotify" in statement:
            os.system("taskkill /f /im EpicGamesLauncher.exe")
            speak("closed spotify")

        elif "open sublime" in statement or "sublime text 3" in statement:
            speak("Opening sublime text 3")
            subprocess.call(
                "C://Program Files//Sublime Text 3//sublime_text.exe")

        elif "notepad" in statement or "open notepad" in statement:
            subprocess.call("C://Windows//System32//notepad.exe")
            speak("opened notepad")

        elif "current brightness" in statement or "what is the current brightness" in statement:
            speak(str(sbc.get_brightness()) + "percent")

        elif there_exists(["play"]):
            search_term = statement.replace("play", '')
            kit.playonyt(search_term)
            speak(f"Here is what I found for {search_term} on youtube")

        elif there_exists(["youtube"]):
            search_term = statement.replace("youtube", '')
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on youtube')

        elif there_exists(["price of"]):
            # strip removes whitespace after/before a term in string
            search_term = statement.lower().split(" of ")[-1].strip()
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

        elif "open vscode" in statement or "open visual studio code" in statement:
            speak("opening visual studio code")
            subprocess.call(
                "C://Users//Rohith JN//AppData//Local//Programs//Microsoft VS Code//Code.exe")

        elif "close vscode" in statement or "close visual studio code" in statement:
            speak("closing visual studio code")
            os.system("taskkill /f /im code.exe")

        elif "tell me a joke" in statement or "joke" in statement:
            joke = (pyjokes.get_joke())
            speak(joke)
            print(joke)

        elif "not funny" in statement or "tell me another one" in statement:
            speak("do you want me to tell another one")

        elif "yes" in statement or "tell me" in statement:
            joke = (pyjokes.get_joke())
            speak(joke)
            print(joke)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            speak("opening gmail")
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
            speak("Gmail is open now")
            time.sleep(5)

        elif "open a new tab in google" in statement or "open new tab" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opened new tab")

        elif there_exists(["search for"]) and 'youtube' not in statement:
            search_term = statement.split("for")[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on google')

        elif "close google" in statement or "shutdown google" in statement:
            os.system("taskkill /f /im chrome.exe")

        elif 'time' in statement or "what is the time" in statement or "what's the time" in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Friday your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather'
                  'in different cities , get top headline news and you can ask me computational or geographical questions too!')

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif "calculator" in statement:
            subprocess.call("calc.exe")

        elif 'Indian news' in statement:
            news = webbrowser.open_new_tab(
                "https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India')
            time.sleep(6)

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif "log off" in statement or "sign out" in statement or "kill switch" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "shutdown" in statement:
            speak("Shutting down your pc, make sure you exit from all applications")
            subprocess.call(["shutdown", "/s"])

        elif "restart" in statement:
            speak("Restarting laptop, make sure you exit from all applications")
            subprocess.call(["shutdown", "/r"])

time.sleep(3)
