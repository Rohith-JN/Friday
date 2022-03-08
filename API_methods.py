import asyncio
from difflib import SequenceMatcher
import platform
from API_creds import *
from telethon.tl.types import InputPeerUser
from telethon import TelegramClient
from telethon import functions
import distance


if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
    async def sendUserMessage(self, response, message):
        client = TelegramClient('session', api_id, api_hash)
        await client.connect()
        result = await client(functions.contacts.GetContactsRequest(
            hash=0
        ))
        for user in result.users:
            try:
                s = SequenceMatcher(None, response, user.first_name)
                print(response, user.first_name)
                print(s.ratio())
                print(distance.levenshtein(response, user.first_name))
                if s.ratio() > 0.75 or distance.levenshtein(response, user.first_name) < 3:
                    receiver = InputPeerUser(user.id, 0)
                    await client.send_message(receiver, message, parse_mode='html')
                else:
                    pass
            except Exception:
                pass
        await client.disconnect()