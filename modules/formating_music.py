from const import (
    LEN_INST,
    INST,
    MAX_SYMBOLS_IN_BIO_NON_PREMIUM,
    MAX_SYMBOLS_IN_BIO_PREMIUM,
    MUSIC_STOPPED,
    MUSIC_DOESNT_PLAYING
)
import modules.spotify_time as timestp

async def format_current_playing(
    current:dict,
    user_is_premium: bool
    ):
    '''
    Docstring for format_current_playing
    
    :param current: currently playing from spotify api
    :type current: dict
    '''
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
    