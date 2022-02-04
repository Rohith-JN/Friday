import requests
from spotifyCreds import spotify_user_id, playlist_id, device_id
from refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.playlist_id = playlist_id
        self.tracks = ""
        self.device_id = device_id

    def find_songs(self):
        print("Finding songs in your playlist...")
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Accept": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response)

    def call_refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
