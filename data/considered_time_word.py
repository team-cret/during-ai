from datetime import timedelta, datetime

considered_time = {
    '오늘' : (timedelta(days=0), timedelta(days=0), True),
    '어제' : (timedelta(days=-1), timedelta(days=-1), True),
    '그제' : (timedelta(days=-2), timedelta(days=-2), True),
    '그저께' : (timedelta(days=-2), timedelta(days=-2), True),
    '내일' : (timedelta(days=1), timedelta(days=1), True),
    '모레' : (timedelta(days=2), timedelta(days=2), True),
    '이번주' : (None, timedelta(days=7), False),
    '작년': (None, timedelta(days=365), False),
    '올해': (None, timedelta(days=365), False),
}

def parse_considered_time(cur_date:datetime, time_word:str) -> str:
    if considered_time[time_word][2]:
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
    else:
        if time_word == '이번주':
            start_date = cur_date - timedelta(days=cur_date.weekday())
            start_date = datetime(
                year=start_date.year,
                month=start_date.month,
                day=start_date.day,
                hour=0,
                minute=0,
                second=0
            )
        elif time_word == '작년':
            start_date = datetime(
                year=cur_date.year - 1,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0
            )
        elif time_word == '올해':
            start_date = datetime(
                year=cur_date.year,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0
            )
        end_date = start_date + considered_time[time_word][1]

    return f'{start_date} ~ {end_date}'