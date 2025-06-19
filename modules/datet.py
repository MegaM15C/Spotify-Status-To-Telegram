import datetime

def give_ho_mi_se_podcast(ms:int):
    td = datetime.timedelta(milliseconds=ms)
    td = int(td.total_seconds())
    hours = td // 3600
    minutes = (td % 3600) // 60
    seconds = td % 60
    
    return f'{hours:01}:{minutes:02}:{seconds:02}'

def give_min_sec_music(ms:int):
    td = datetime.timedelta(milliseconds=ms)
    td = int(td.total_seconds())
    minutes = (td % 3600) // 60
    seconds = td % 60
    
    return f'{minutes:02}:{seconds:02}'