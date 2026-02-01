import spotipy
import os


async def initialie_spotify_client():
    '''
    initialize spotify client.
    1. If not exists session, create new
    2. Else return spotify
    '''
    spotify = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            scope="user-read-currently-playing",
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('REDIRECT_URL'),
            username=os.getenv('SPOTIFY_USERNAME'),
        )
    )
    return spotify