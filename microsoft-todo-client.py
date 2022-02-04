from importlib.resources import contents
import requests
from GraphAPIcreds import client_id, client_secret, refresh_token
from refresh_todo import Refresh


class Todo:
    def __init__(self):
        self.client_id = client_id,
        self.client_secret = client_secret,
        self.refresh_token = refresh_token,
        self.access_token = ''

    def getTodoLists(self):
        query = "https://graph.microsoft.com/v1.0/me/todo/lists"
        response = requests.get(query,
                                headers={"client-request-id": "97dc3f21-a10d-d740-c2c2-483f4cc58aa7",
                                         "content-type": "application/json;odata.metadata=minimal;odata.streaming"
                                                         "=true;IEEE754Compatible=false;charset=utf-8",
                                         "request-id": "15617ee4-2c65-46bb-a538-7aa595101ac6",
                                         "Authorization": "Bearer {}".format(self.access_token)},
                                data={
                                    'status': 'Tasks.Read Tasks.Read.Shared Tasks.ReadWrite Tasks.ReadWrite.Shared '
                                              'offline_access '
                                })
        response_json = response.json()
        for i in response_json['value']:
            name = i['displayName']
            id = i['id']
            print(f'{name} : {id}')
        

    def refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.access_token = refreshCaller.refresh()


a = Todo()
a.refresh()
a.getTodoLists()
