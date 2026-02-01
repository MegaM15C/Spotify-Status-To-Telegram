import asyncio
import time
import os
import spotipy
from dotenv import load_dotenv
from telethon import TelegramClient, functions
import modules.datet as timestp
from modules.auth import get_session

load_dotenv()

# Init Spotify client API
spotify = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        scope="user-read-currently-playing",
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URL'),
        username=os.getenv('SPOTIFY_USERNAME'),
    )
)

inst = ' | inst: @dngrmax'
user = '@dngrmax'


async def main():
    client = await get_session()

    while True:
        try:
            current = spotify.current_user_playing_track()
            # print(current)

            if not current:
                muzon = "ᯤ Spotify isn't playing"
            elif not current['is_playing']:
                muzon = "ᯤ Spotify is paused"
            elif current["currently_playing_type"] == "track":
                timestamp = timestp.give_min_sec_music(current['progress_ms'])
                track = current["item"]["name"]
                artist = current["item"]["artists"][0]["name"]
                muzon = f"ᯤ Spotify | {timestamp} | {artist} - {track}"
            elif current["currently_playing_type"] == "episode":
                timestamp = timestp.give_ho_mi_se_podcast(ms=current['progress_ms'])
                muzon = f"ᯤ Spotify is playing a podcast | {timestamp}"

            if len(muzon) >= 53:
                muzon = muzon[:50] + '...' + inst
            else:
                muzon += inst

            full = await client(functions.users.GetFullUserRequest('me'))
            stat = full.full_user.about

            if muzon != stat:
                await client(functions.account.UpdateProfileRequest(about=muzon))

            await asyncio.sleep(15)

        except Exception as e:
            print(e)
            await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
