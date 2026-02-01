from const import (
    LEN_INST,
    INST,
    MAX_SYMBOLS_IN_BIO_NON_PREMIUM,
    MAX_SYMBOLS_IN_BIO_PREMIUM,
    MUSIC_STOPPED,
    MUSIC_DOESNT_PLAYING
)
from typing import Any
import modules.spotify_time as timestp

async def format_current_playing(
    current: Any,
    user_is_premium: bool
) -> str:
    """
    Format the current Spotify playback state into a string suitable
    for a Telegram profile bio.

    Logic:
    - If there is no active playback, return a predefined "not playing" message.
    - If playback exists but is paused, return a predefined "stopped" message.
    - If a track is playing, include its progress (MM:SS), artist, and title.
    - If a podcast episode is playing, include its progress (HH:MM:SS).
    - After formatting, pass the result to the bio-cropping helper to ensure
      it fits Telegram limits depending on Premium status.

    Args:
        current (Any): Raw "currently playing" object returned by the Spotify API.
                       Can be None or a dict with playback details.
        user_is_premium (bool): Indicates whether the Telegram user has Premium,
                                which affects the maximum allowed bio length.

    Returns:
        str: Final formatted and cropped string ready to be set as the Telegram bio.
    """
    if not current: # if music doesn't playing
        music = MUSIC_DOESNT_PLAYING
        
    elif not current['is_playing']: # if music is stopped
        music = MUSIC_STOPPED
        
    elif current["currently_playing_type"] == "track":
        # calculate progress if it's track
        timestamp = timestp.give_min_sec_music(current['progress_ms'])
        track = current["item"]["name"]
        artist = current["item"]["artists"][0]["name"]
        music = f"ᯤ Spotify | {timestamp} | {artist} - {track}"
        
    elif current["currently_playing_type"] == "episode":
        # calculate progress if it's podcast
        timestamp = timestp.give_ho_mi_se_podcast(ms=current['progress_ms'])
        music = f"ᯤ Spotify is playing a podcast | {timestamp}"
    
    return await _crop_bio(user_is_premium=user_is_premium, music=music)



async def _crop_bio(
    user_is_premium: bool,
    music: str
):
    '''
    Docstring for crop_bio
    Crop music string if it's too long
    
    :param user_premiun_bool: Premium User (True) or no (False)
    :type user_premiun_bool: bool
    :param music: String with info about currently playing
    :type music: str
    '''
    if not user_is_premium:
        if len(music) >= (MAX_SYMBOLS_IN_BIO_NON_PREMIUM - LEN_INST):
            music = music[
                :MAX_SYMBOLS_IN_BIO_NON_PREMIUM -3 - LEN_INST
                ] + '...' + INST
        else:
            music += INST
    else:
        if len(music) >= (MAX_SYMBOLS_IN_BIO_PREMIUM - LEN_INST):
            music = music[
                :MAX_SYMBOLS_IN_BIO_PREMIUM -3 - LEN_INST
                ] + '...' + INST
        else:
            music += INST
            
    return music
    