import time
import os
import typing
import spotipy
import asyncio

import modules.datet as timestp

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from telethon.sync import TelegramClient
from telethon import functions, types


load_dotenv()

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-currently-playing",
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URL'),
        username=os.getenv('SPOTIFY_USERNAME'),
    )
)
inst = ' | inst: @dngrmax'
user = '@' + 'dngrmax'
current_playing = typing.List[typing.Union[str, str, str]]


def update_status(_current_playing):
    current = spotify.current_user_playing_track()
    print()
    print(current)
    if current == None:
        muzon = "ᯤ Spotify isn't playing"
    elif current['is_playing'] == False:
        muzon = "ᯤ Spotify is paused"
        
    elif current["currently_playing_type"] == "track":
        timestamp = timestp.give_min_sec_music(current['progress_ms'])
        
        track = current["item"]["name"]
        #album = current["item"]["album"]["name"]
        artist = current["item"]["artists"][0]["name"]
        muzon = f"ᯤ Spotify | {timestamp} | {artist} - {track}"
        
    elif current["currently_playing_type"] == "episode":
        timestamp = timestp.give_ho_mi_se_podcast(ms = current['progress_ms'])
        muzon = f"ᯤ Spotify is playing a podcast | {timestamp}"
        

    if len(muzon) >= 53:                   
        muzon = muzon[:50] + '...' + inst
    else:
        muzon += inst

    with TelegramClient('host', os.getenv('TG_API_ID'), os.getenv('TG_API_HASH')) as client:
        full = client(functions.users.GetFullUserRequest(user))
        stat = full.full_user.about
        if muzon != stat:
            client(functions.account.UpdateProfileRequest(about=muzon))

    return 




if __name__ == '__main__':
    while True:
        try:
            while True:
                # print("Получаю обновления")
                current_playing = (update_status(current_playing)) 
                time.sleep(15)

        except Exception as e:
            print(e)
            time.sleep(30)
input('Press ENTER to exit')
