from API_creds import *
import requests
from telethon.tl.types import InputPeerUser
from telethon import TelegramClient


class Methods:

    def __init__(self):
        self.api_id = api_id,
        self.api_hash = api_hash,
        self.token = token,
        self.user_id_1 = user_id_1,
        self.phone = phone
        self.refresh_token = refresh_token
        self.scope = scope
        self.client_secret = client_secret
        self.client_id = client_id,
        self.refresh_token = refresh_token,
        self.access_token = ''

    def refresh(self):
        query = "https://login.microsoftonline.com/{}/oauth2/token".format(tenant_id)
        response = requests.post(query,
                                 data={"client_id": client_id,
                                       "refresh_token": refresh_token,
                                       "redirect_uri": 'https://github.com',
                                       "grant_type": "refresh_token",
                                       "client_secret": client_secret
                                       },
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})

        response_json = response.json()
        return response_json['access_token']

    def getTodoLists(self):
        query = "https://graph.microsoft.com/v1.0/me/todo/lists"
        response = requests.get(query,
                                headers={
                                    "content-type": "application/json",
                                    "Authorization": "Bearer {}".format(self.access_token)},
                                )
        response_json = response.json()
        print(response)
        print(response_json)

    def refresh(self):
        print("Refreshing token")
        refreshCaller = Methods()
        self.access_token = refreshCaller.refresh()

    async def sendPersonalMessage(self, message, user_id):
        client = TelegramClient('session', api_id, api_hash)
        await client.connect()
        if not client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        try:
            receiver = InputPeerUser(user_id, 0)
            await client.send_message(receiver, message, parse_mode='html')
        except Exception as e:
            print(e)
        client.disconnect()


    
