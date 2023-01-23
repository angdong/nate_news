from typing import List
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
from crawl import NateNews

import datetime as dt
import pandas as pd

# TODO: make *.ipynb for instruct how to use utils.py
LINK = 'https://news.nate.com/view/'
COLUMNS = [
    'title',
    'category',
    'press',
    'date',
    'content',
    'url',
]

def get_news_df(
    news_list: List[NateNews]
):
    """make `pd.DataFrame` with `news_list`

    Returns:
        pd.DataFame: DataFrmae w.r.t `news_list`
    """    
    info_list = [news.get_info() for news in news_list]
    return pd.DataFrame(info_list, columns=COLUMNS)

def get_news(
    url_list: List[str]
):
    """Return `NateNews` list

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

def get_urls(
    date1: Union[int, None]=None,
    date2: Union[int, None]=None,
    artc1: Union[int, None]=None,
    artc2: Union[int, None]=None,
):
    """get url list
    
    Desc:
        url list
        eg:
            `date1`: `article1` ~ `article2`
            `dateN`: `article1` ~ `article2`
            \n\t\t...
            `date2`: `article1` ~ `article2`

    Args:
        date1 (Union[int, None], optional):
            None -> `datetime.datetime.now()`
        date2 (Union[int, None], optional): 
            None -> `date1`
        artc1 (Union[int, None], optional):
            None -> 1: first article of that day
        artc2 (Union[int, None], optional):
            None -> last article of that day

    Returns:
        List[str]: url list
    """    
    date1 = date1 if date1 else int(dt.datetime.now().strftime('%Y%m%d'))
    date2 = date2 if date2 else date1
    artc1 = artc1 if artc1 and artc1 > 0 else 1

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
    """get date list

    Args:
        `date1` (int): first date
        `date2` (int): last date

    Returns:
        List[int]: date list from `date1` to `date2`
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
    artc2: Union[int,None],
    date: int,
):
    """get article list

    Args:
        `artc1` (int): first article in NateNews
        `artc2` (Union[int,None]): last article in NateNews
            None: `artc2` = latest article on `date`
        `date` (int): the day you want to crawl

    Returns:
        List[int]: article list from `artc1` to `artc2`
    """
    max_article = NateNews.get_recent(date)
    artc1 = artc1 if artc1 < max_article else max_article

    if not artc2 or artc2 > max_article:
        artc2 = max_article
    return [artc for artc in range(artc1, artc2+1)]
