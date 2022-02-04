from GraphAPIcreds import refresh_token, scope, client_id, client_secret, tenant_id
import requests


class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.scope = scope
        self.client_secret = client_secret

    def refresh(self):
        query = "https://login.microsoftonline.com/{}/oauth2/token".format(tenant_id)
        response = requests.post(query,
                                 data={"client_id" : client_id,
                                       "scope": 'Tasks.Read%20Tasks.Read.Shared%20Tasks.ReadWrite%20Tasks.ReadWrite.Shared%20offline_access',
                                       "refresh_token": refresh_token,
                                       "redirect_uri": 'https://github.com',
                                       "grant_type": "refresh_token",
                                       "client_secret": client_secret
                                       },
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})

        response_json = response.json()
        return response_json['access_token']

a = Refresh()
a.refresh()