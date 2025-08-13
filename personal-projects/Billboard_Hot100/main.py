from bs4 import BeautifulSoup
import requests
import os
from pprint import pprint
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
URL = "https://www.billboard.com/charts/hot-100/"
year_info = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

response = requests.get((URL + year_info))
soup = BeautifulSoup(response.text, "html.parser")
song_title = soup.select("li h3.c-title")
list_song = [song.getText().strip() for song in song_title]
year_date = year_info.split("-")[0]
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path="token.txt",show_dialog=True))
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"Billboard {year_date} Hits", public=False)
playlist_id = playlist["id"]
song_uris = []
for song in list_song:
    results = sp.search(q=f"track:{song} year:{year_date}", type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        print(f"This song {song} is not available.")

track = sp.playlist_add_items(playlist_id, song_uris)
pprint(track)