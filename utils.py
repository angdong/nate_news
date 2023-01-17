import datetime as dt

def get_date(date1: str, date2: str=None):
    if not date2:
        return [date1]
    