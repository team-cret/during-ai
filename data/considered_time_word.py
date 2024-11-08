from datetime import timedelta, datetime

considered_time = {
    '오늘' : (timedelta(days=0), timedelta(days=0)),
    '어제' : (timedelta(days=-1), timedelta(days=-1)),
    '그제' : (timedelta(days=-2), timedelta(days=-2)),
    '그저께' : (timedelta(days=-2), timedelta(days=-2)),
    '내일' : (timedelta(days=1), timedelta(days=1)),
    '모레' : (timedelta(days=2), timedelta(days=2)),
    '이번주' : (timedelta(days=0), timedelta(days=6)),
    '작년': (timedelta(days=-365), timedelta(days=0)),
}

def parse_considered_time(cur_date:datetime, time_word:str) -> str:
    start_date = datetime(
        year=cur_date.year,
        month=cur_date.month,
        day=cur_date.day,
        hour=0,
        minute=0,
        second=0
    ) + considered_time[time_word][0]

    end_date = datetime(
        year=cur_date.year,
        month=cur_date.month,
        day=cur_date.day,
        hour=23,
        minute=59,
        second=59
    ) + considered_time[time_word][1]

    return f'{start_date} ~ {end_date}'