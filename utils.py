import datetime as dt

def get_date(date1: int, date2: int=None, /):
    """
    Return list of date(s)
    
    :param `date1`: first date
    :param `date2`: (Optional) second date
    
    :return:
        date list from `date1` to `date2`
    """
    if not date2:
        return [date1]
    
    date:int = date1
    date_list = list()
    while date <= date2:
        date_list.append(date)
        date = dt.datetime.strptime(str(date), "%Y%m%d") + dt.timedelta(days=1)
        date = int(date.strftime('%Y%m%d'))
    
    return date_list
