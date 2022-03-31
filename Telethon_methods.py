from difflib import SequenceMatcher
import json
from API_keys import *
from telethon.tl.types import InputPeerUser
from telethon import TelegramClient
from telethon import functions, types
import distance
from Friday_Functions import *

class Methods:

    def __init__(self):
        self.api_id = api_id,
        self.api_hash = api_hash,
        self.phone = phone

    async def authorize(self, client):
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        await client.disconnect()

    #send-user-message
    async def sendUserMessage(self, response):
        isSent = False
        client = TelegramClient('session', api_id, api_hash)
        await client.connect()
        result = await client(functions.contacts.GetContactsRequest(
            hash=0
        ))
        for user in result.users:
            try:
                s = SequenceMatcher(None, response, user.first_name)
                if s.ratio() > 0.75 or distance.levenshtein(response, user.first_name) < 3:
                    speak("What do you wanna send?")
                    message = takeCommand()
                    isSent = True
                    receiver = InputPeerUser(user.id, 0)
                    await client.send_message(receiver, message, parse_mode='html')
                else:
                    pass
            except Exception:
                pass
        await client.disconnect()
        if isSent:
            speak("Message sent successfully")
        else:
            speak("Could not find that user in your contacts")
