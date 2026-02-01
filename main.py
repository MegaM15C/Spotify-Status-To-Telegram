import asyncio

# from telethon import functions, errors
import modules.spotify_time as timestp
from modules.telegram import (
    get_session,
    update_telegram_status,
    get_user_info
)
from typing import Any
from modules.spotify import initialie_spotify_client
from modules.formating_music import _crop_bio, format_current_playing


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
            current = await _get_spotify_track()
            full_user_info, user_is_premium = await get_user_info(client)
            
            music = await format_current_playing(
                current=current,
                user_is_premium=user_is_premium
                )
            
            await update_telegram_status(client, music, full_user_info)
            
            # wait 15 sec for security
            await asyncio.sleep(15)
        
        except Exception as e:
            print(current)
            print(e)
            await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
