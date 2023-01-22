from typing import List
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
from crawl import NateNews

import datetime as dt

LINK = 'https://news.nate.com/view/'

def get_urls(
    date1: Union[int, None]=None,
    date2: Union[int, None]=None,
    artc1: Union[int, None]=None,
    artc2: Union[int, None]=None,
):
    date1 = date1 if date1 else int(dt.datetime.now().strftime('%Y%m%d'))
    date2 = date2 if date2 else date1
    artc1 = artc1 if artc1 else 1

    urls = [
        f"{LINK}{date}n{str(num).zfill(5)}"
        for date in _get_date_list(date1, date2)
        for num in _get_artc_list(artc1, artc2, date)
    ]
    return urls


def _get_date_list(
    date1: int,
    date2: int, 
):
    """get date list from `date1` to `date2`

    Args:
        `date1` (int): first date
        `date2` (int, optional): last date

    Returns:
        List[str]: date list from `date1` to `date2`
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

def _get_artc_list(
    artc1: int,
    artc2: Union[str, None],
    date: int,
):
    if not artc2:
        artc2 = NateNews.get_recent(date)
    return [artc for artc in range(artc1, artc2+1)]

# url = f"{LINK}{date}n{str(num).zfill(5)}"

def get_news(
    url_list: List[Union[NateNews, None]]
):
    """Return requests of url list

    Args:
        url_list (List[str]): url list to be requested

    Returns:
        List[Union[Response, None]]:
            1. NateNews: Normal Request
            2. None: Abnormal Request(won't get that page)
    """
    with ThreadPoolExecutor(max_workers=10) as mult:
        _news_list = list(mult.map(NateNews.create, url_list))
    news_list = [news for news in _news_list if news]
    return news_list
