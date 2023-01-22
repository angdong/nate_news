import requests 
import datetime as dt
from bs4 import BeautifulSoup as bs

LINK = 'https://news.nate.com/view/'

# TODO: return DataFrame form news
# TODO: Real-time crawl(with same domain)
"""
    1. same category
    2. same contents(search..?)
    3. same press
    4. etc.
"""

class NateNews:
    """
    Crawler for natenews
    
    :param url: news url, form should be https://news.nate.com/view/{DATE}n{ARTICLE_NUM}
    
    :var:
        `self.day`: day format(%Y%m%d)
        `self.post_num`: order of article in that day
        `self.content`: article content
        `self.title` : article title
        `self.category` : category of news 
    """    
    def __init__(self, url:str):        
        res = requests.get(url)
        assert res.status_code == 200
        
        html = res.text
        # self.day = int(url.split('/')[-1].split('n'))
        # self.post_num = int(url.split('/')[-1].split('n'))

        self.content = bs(html, 'html.parser')
        # self.title = self._get_title()
        # self.category = self._get_category()
        # self.time = self._get_time()
        # self.press = self._get_press()

    def _get_contents(self):
        # TODO: data cleaning
        # TODO: <p> tag handling
        # TODO: accumulate all the attributes below
        article = self.content.find('div', {'id': 'realArtcContents'})
        text = article.text

        return text
    
    def get_title(self):
        title = self.content.find('h3', {'class': 'articleSubecjt'})
        return title.text
    
    def _get_category(self):
        nav = self.content.find('div', {'id': 'mediaSubnav'})
        category = nav.find('h3')
        return category.text
    
    def _get_time(self):
        # TODO: get article of same date
        
        _time = self.content.find('span', {'class': 'firstDate'})
        _time = _time.find('em').text
        time = dt.datetime.strptime(_time, "%Y-%m-%d %H:%M")
        return time.text
    
    def _get_press(self):
        # TODO: get hyperlink of same press

        press = self.content.find('a', {'class': 'medium'})
        return press.text
    
    @staticmethod
    def get_recent(date: int):
        req = requests.get(f'https://news.nate.com/recent?mid=n0100&type=c&date={date}')
        content = bs(req.text, 'html.parser')
        _recent = content.find_all('div', {'class': 'mlt01'})
        
        latest = None
        for news in _recent:
            # recent = //news.nate.com/view/{YYYY}{mm}{dd}n{NNNNN}?mid=n0100
            recent = int(news.find('a')['href'].split('?')[0][-5:])
            if not latest or latest < recent:
                latest = recent
        return latest # return latest article number

    @classmethod
    def create(
        cls,
        url:str
    ):
        new_class = cls(url)
        article = new_class.content.find(
            'div',
            {'id': 'RealArtcContents'}
        )
        if not article:
            article = new_class.content.find(
                'div',
                {'id': 'articleContetns'}
            )
        if not article:
            return None
        
        which_news = new_class.content.find(
            'a',
            {'class': 'svcname'}
        ).text
        if which_news == '뉴스':
            return new_class
        else:
            return None
