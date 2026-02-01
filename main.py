import asyncio

from modules import (
    # Telethon features
    get_session,
    update_telegram_status,
    get_user_info,
    
    # Spotipy init
    initialie_spotify_client,
    
    # formatting currently playing
    format_current_playing
)
from typing import Any
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = await get_session()
    spotify = await initialie_spotify_client()
    
    async def _get_spotify_track() -> (Any | None):
        '''
        gets spotify currently playing from '/v1/me/player/currently-playing'
        Returns: 
        '''
        # don't block loop
        return await asyncio.to_thread(spotify.current_user_playing_track)
    
    while True:
        try:
            current = await _get_spotify_track() # get currently playing
            full_user_info, user_is_premium = await get_user_info(client) # get user info in telegram
            
            music = await format_current_playing( # format currently playing
                current=current,
                user_is_premium=user_is_premium
                )
            
            await update_telegram_status(
                client,
                music,
                full_user_info
                ) # update status 
            
            # Wait 15 seconds to avoid being blocked for flooding
            await asyncio.sleep(15)
        
        except Exception as e:
            print(current)
            print(e)
            await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
