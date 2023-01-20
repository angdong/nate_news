from typing import List
from concurrent.futures import ThreadPoolExecutor

import datetime as dt
import requests


def get_date_list(
    date1: int,
    date2: int=None, 
):
    """_summary_

    Args:
        `date1` (int): first date
        `date2` (int, optional): second date

    Returns:
        List[str]: date list from `date1` to `date2`
    """    
    """
    Return list of date(s)
    
    :param `date1`: first date
    :param `date2`: (Optional) second date
    
    :return:
        date list from `date1` to `date2`
    """
    
    if not date2:
        return [date1]
    
    assert date2 > date1
    date:int = date1
    date_list = list()
    
    while date <= date2:
        date_list.append(date)
        date = dt.datetime.strptime(str(date), "%Y%m%d") + dt.timedelta(days=1)
        date = int(date.strftime('%Y%m%d'))
    
    return date_list

def multi_request(
    date_list: List[str]
):
    with ThreadPoolExecutor(max_workers=10) as mult:
        req_list = list(mult.map(requests.get, date_list))
    return req_list