CODE ERRORS AND UNFINISHED CODE AND NEW FEATURES

#current location
elif there_exists(["current location","location","where am i","where am i right now"]) in statement:
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city = data["city"].split(',')
    global city
    state = data["region"].split(',')
    speak(city+"," + state)
    print(city+"," + state)

#weather
options = ["what is the weather","weather","climate","Friday what is the weather","climate","what is the weather right now"]
elif:
    for i in options in statement:
        try
        api_key="8ef61edcf1c576d65d836254e11ea420"
        global api_key
        base_url="https://api.openweathermap.org/data/2.5/weather?"
        global base_url
        complete_url=base_url+"appid="+api_key+"&q="+location
        response = requests.get(complete_url)
        x=response.json()
        if x["cod"]!="404":
            y=x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(" Temperature in kelvin unit is " +
                str(current_temperature) +
                "\n humidity in percentage is " +
                str(current_humidiy) +
                "\n description  " +
                str(weather_description))
            print(" Temperature in kelvin unit = " +
                str(current_temperature) +
                "\n humidity (in percentage) = " +
                str(current_humidiy) +
                "\n description = " +
                str(weather_description))
        else:
            speak(" City Not Found ")

        except Exception:
                try:
                    client = python_weather.Client(format=python_weather.IMPERIAL)
                    weather = await client.find(location)
                    speak(weather.current.temperature)
                    for forecast in weather.forecast:
                        speak(str(forecast.date), forecast.sky_text, forecast.temperature)
                    await client.close()
                else:
                    speak(" City Not Found ")

        except Exception:
                try:
                    URL = f"https://www.google.com/search?q={location}"
                    req = requests.get(URL)
                    sav = BeautifulSoup(req.text,"html.parser")
                    update = sav.find("div",class_=_"BNeawe").text
                    speak(update)
                else:
                    speak(" City Not Found ")
#recording audio
import sounddevice as sd
from scipy.io.wavfile import write

def RecordAudio(Length):
    seconds = 10
    Length = seconds
    fs = 44100
    print("Recording")
    speak("Recording")
    myrecording = sd.rec(int(int(Length) * fs), samplerate=fs, channels=2)
    time.sleep(int(Length))
    print("Recoding complete")
    speak("Recording complete")
    if "play recording" in statement:
        sd.play(myrecording)
        print("playing recorded audio")
    elif "save recording" in statement:
        write.('output.wav', fs, myrecording)
    time.sleep(int(Length))

elif "record audio" in statement:
    command = RecordAudio

#Fixing alarm
import winsound
import pygame
import os

        elif "set an alarm for" in statement:
            search_term = statement.replace("set an alarm for",'')
            time = search_term.split(":", )
            alarm_hour = time[0]
            alarm_minute = time[1]
            speak("am or pm")
            if "pm" in statement:  
                alarm_hour += 12

            elif alarm_hour == 12 and "am" in statement: 
                alarm_hour -= 12
                speak(f"Waiting for time: {alarm_hour}:{alarm_minute}")
                print(f"Waiting for time: {alarm_hour}:{alarm_minute}")

            else:
                pass

            while True: 

                
                if alarm_hour == datetime.datetime.now().hour and alarm_minutes == datetime.datetime.now().minute:

                    speak("\nIt's the time!")
                    alarm_dir = "C:\\Users\\Rohith JN\\Music\\music\\Apple alarm ringtone.mp3"
                    file = os.startfile(alarm_dir)
                    if "pause" in statement or "stop" in statement:
                        pygame.mixer.music.pause(alarm_dir)
                    break

#checking if charger is plugged in
source = power.POWER_TYPE_BATTERY
if source = True
speak("Charger is plugged in")

#playing music    
def PlayMusic():
    root, dirs, files = next(os.walk('tracks/'))
    
    pygame.mixer.init()
    
    for name in files:
        name = 'tracks/'+str(name)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():
            if Interface == "Voice":
                print "Listening"
                Command = Listen(r)
                print "-" + str(Command)
                KnownCommands(Command, r, NextLine, ScoreIndexes)  
            else:
                Command = str(raw_input("Command: "))
                print "-" + str(Command)
                KnownCommands(Command, r, NextLine, ScoreIndexes)
            pygame.time.Clock().tick(5)
     
#stopping music6
def StopMusic():
    pygame.mixer.music.stop()

#pausing music
def PauseMusic():
    pygame.mixer.music.pause()

#resuming music
def ResumeMusic(Loopme):
    pygame.mixer.music.play
    while pygame.mixer.music.get_busy():
        if Interface == "Voice":
            print "Listening"
            Command = Listen(r)
            print "-" + str(Command)
            KnownCommands(Command, r, NextLine, ScoreIndexes)  
        else:
            Command = str(raw_input("Command: "))
            print "-" + str(Command)
            KnownCommands(Command, r, NextLine, ScoreIndexes)
        pygame.time.Clock().tick(5)


#setting an alarm
def CheckAlarm():
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        for j in range(0,11):
            speak("alarm")

#Setting volume and increasing,decreasing volume command,function
import alsaaudio
import sys

m = alsaaudio.Mixer()
vol = m.getvolume()

def getVolume():
    global vol
    return vol[0]

def increase(n):
    global vol
    if (vol[0] + n)>100:
        vol[0] = 100 - n
    m.setvolume(vol[0] + n)
    vol = m.getvolume()
    speak("Volume increased to" + str(vol[0]) + "percent")

def decrease(n):
    global vol
    if (vol[0] - n)>100:
        vol[0] = 100 + n
    m.setvolume(vol[0] - n)
    vol = m.getvolume()
    speak("Volume decreased to" + str(vol[0]) + "percent")


def setVolume(n):
    global vol
    m.setvolume(n)
    vol = m.getvolume()
    speak("Volume set to" + str(vol[0]) + "percent")

elif there_exists(["increase volume to"]):
    n = statement.replace("increase volume to",'')
    command = increase(n)

elif there_exists(["decrease volume to"]):
    n = statement.replace("decrease volume to",'')
    command = decrease(n)

elif there_exists(["set volume to"]):
    n = statement.replace("set volume to",'')
    command = setVolume(n)

#fix timer bug
elif str(search_term) in list(time) == "hours":
	speak("for how many hours should I wait")
	hours = statement
	for i in range(hours):
	   print(str(hours - i) + "hours remaining")
	   time.sleep(3600)
	else:
        speak("wrong input")

elif there_exists(["set a timer for seconds"]):
    x = statement.lower().split(" ",6)
	   search_term = x[ 4 ]
        speak(f"setting a timer for {search_term} seconds")
        for i in range(int(search_term)):
            print(int(search_term - i) + " seconds remaining")
            time.sleep(1)
            speak("Timer done")

#fix and the battery counter should only repeat once
elif percent == 20:
    run_once = 0
    while True:
        if run_once == 0:
            speak("Battery percentage is at 20%, plug in the charger")
            run_once = 1

elif percent == 100:
	speak("Battery percentage is at 100%, remove the charger if plugged in")

elif percent < 20 or percent == 20:
	speak("Battery percentage is below 20%, plug in the charger")

#timer example no 2
elif there_exists(["set a timer for seconds"]):
    search_term = statement.lower().split("set a timer for seconds","")
    speak(f"setting a timer for {search_term} seconds")
    for i in range(int(search_term)):
        print(int(search_term - i) + " seconds remaining")
        time.sleep(1)
        speak("Timer done")

#Another method to play specified music
import playsound

elif there_exists(["play"]) in statement:
    search_term = statement.replace("play", '')
    music_dir = "C:\\Users\\Rohith JN\\Music\\music"
    playsound(search_term + ".mp3")
    speak(f"playing {search_term}")

#Playing random music from library
import playsound
elif "play random music" in statement or "play music" in statement:
    music_dir = "C:\\Users\\Rohith JN\\Music\\music"
    playsound.random.choice(music_dir)
    speak("playing music")

#getting the answers from google

elif "Friday" in statement:
    statement = statement.replace("Friday",'')
    client = wolframalpha.Client("8ef61edcf1c576d65d836254e11ea420")
    res = client.query(statement)
    ans = next(res.results).text
    print(ans)
    speak(ans)

    except Exception:
        try:
            statement = statement.replace("Friday",'')
            resutls = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)
            
        except Exception:
            statement = statement.replace('Friday','')
            webbrowser.open('https://google.com/?#q=' + statement)
            
#getting geographical answers
elif 'ask' in statement or "what questions can you answer" in statement:
    speak('I can answer to computational and geographical questions and what question do you want to ask now')
    question=takeCommand()
    app_id="8ef61edcf1c576d65d836254e11ea420"
    client = wolframalpha.Client('8ef61edcf1c576d65d836254e11ea420')
    res = client.query(question)
    answer = next(res.results).text
    speak(answer)
    print(answer)

#getting mathematical answers
elif "calculate" in statement:
    speak("what should I calculate")
    gh = takeCommand().lower()
    if statement != int: 
        exit
    else:
        continue
    app_id="R2K75H-7ELALHR35X"
    client = wolframalpha.Client('R2K75H-7ELALHR35X')
    res = client.query(gh)
    answer = int((next(res.results).text))
    speak(answer)
    print(answer)


#scraping answers from wikipedia using wikipedia module
if 'wikipedia' in statement:
    speak('Searching Wikipedia...')
    statement =statement.replace("wikipedia", "")
    results = wikipedia.summary(statement, sentences=3)
    speak("According to Wikipedia")
    print(results)
    speak(results)

#scraping the web for mathematical answers
import requests
from bs4 import BeautifulSoup
r = requests.get("fill")
soup = BeautifulSoup(r.content, 'lxml')
result = soup.find_all('div', class_="fill")
print(result)

#Brightness problem
#Brightness module
current_brightness = sbc.get_brightness()

elif "increase brightness to" in statement:
    n = statement.replace('increase brightness to', '')
    if (current_brightness[0] + n)>100:
        current_brightness[0] = 100 - n
    sbc.set_brightness(current_brightness[0] + n)
    current_brightness = sbc.get_brightness()
    speak("Brightness increased to" + str(current_brightness[0]) + "percent")

elif "decrease brightness to" in statement:
    n = statement.replace("decrease brightness to",'')
    if (current_brightness[0] - n)>100:
        current_brightness[0] = 100 + n
    sbc.fade_brightness(current_brightness[0] - n)
    current_brightness = sbc.get_brightness()
    speak("Brightness decrease to" + str(current_brightness[0]) + "percent")

elif "set brightness to" in statement:
    n = statement.replace("set brightness to",'')
    sbc.set_brightness(n)
    current_brightness = sbc.get_brightness()
    speak("Brightness set to" + str(current_brightness[0]) + "percent")  


#Fix screenshot bug
import pyscreenshot

elif "take a screenshot" in statement or "screen shot" in statement:
    image = pyscreenshot.grab()
    if "show screen shot" in statement or "show image" in statement:
        image.show()
    else:
        speak("Sorry could not open image")
        if "save screenshot" in statement or "save image" in statement:
            speak("How do you wanna save the image as")
            if "save the image as" in statement:
                search_term = statement.replace("Save the image as",'')
                image.save("C:\\Users\\Rohith JN\\Videos\\Captures\\" + search_term)
        else:
            speak("Could not save image")
#Playing specified music from directory
elif there_exists(["play"]) in statement:
    search_term = statement.replace("play",'')
    music_dir = "C:\\Users\\Rohith JN\\Music\\music"
    file = os.path.join(music_dir(os.listdir(music_dir))
    mixer.init()
    mixer.music.load(search_term)
    mixer.music.play()

#Fix playing random music from directory bug
elif "play random music" in statement or "play music" in statement:
    music_dir = "C:\\Users\\Rohith JN\\Music\\music"
    file = os.startfile(os.path.join(music_dir, random.choice(os.listdir(music_dir))






    