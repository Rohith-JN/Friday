from API_creds import *
from telethon.tl.types import InputPeerUser
from telethon import TelegramClient

class Methods:

    def __init__(self):
        self.api_id = api_id,
        self.api_hash = api_hash,
        self.token = token,
        self.user_id_1 = user_id_1,
        self.phone = phone
        self.access_token = ''

    async def sendPersonalMessage(self, message, user_id):
        client = TelegramClient('session', api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        try:
            receiver = InputPeerUser(user_id, 0)
            await client.send_message(receiver, message, parse_mode='html')
        except Exception as e:
            print(e)
        await client.disconnect()

    async def sendGroupMessage(self, entity,message):
        client = TelegramClient('session', api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        try:
            await client.send_message(entity=entity, message=message)
        except Exception as e:
            print(e)
        await client.disconnect()