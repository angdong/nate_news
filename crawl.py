import requests 
import datetime as dt
from bs4 import BeautifulSoup as bs

LINK = 'https://news.nate.com/view/'

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
        self.day = int(url.split('/')[-1].split('n'))
        self.post_num = int(url.split('/')[-1].split('n'))

        self.content = bs(html, 'html.parser')
        self.title = self._get_title()
        self.category = self._get_category()
        self.time = self._get_time()
        self.press = self._get_press()

    def _get_contents(self):
        # TODO: data cleaning
        # TODO: <p> tag handling
        # TODO: accumulate all the attributes below
        article = self.content.find('div', {'id': 'realArtcContents'})
        text = article.text

        return text
    
    def _get_title(self):
        title = self.content.find('h3', {'class': 'articleSubecjt'})
        return title
    
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
    
    # TODO: staticmethod handling -> move to other dir?
    @staticmethod
    def get_contents(url):
        """get contents

        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """        
        res = requests.get(url)
        assert res.status_code == 200 
        html = res.text
        content = bs(html, 'html.parser')
        article = content.find('div', {'id': 'realArtcContents'})
        return article.text
    
    @staticmethod
    def get_list_contents(
        date: int,
        nth_artc: int=1,
        num_artc: int=99999,
    ):
        content_list = list()
        none_list = list()
        flag = 0
        for num in range(nth_artc, nth_artc + num_artc):
            url = f"{LINK}{date}n{str(num).zfill(5)}"
            res = requests.get(url)
            html = res.text
            content = bs(html, 'html.parser')
            article = content.find(
                'div',
                {'id': 'realArtcContents'}
            )
            if not article:
                article = content.find(
                    'div',
                    {'id': 'articleContetns'}
                )
            if not article:
                print(url)
                none_list.append(url)
                if flag == 10:
                    break
                flag += 1
            else:
                content_list.append(article.text)
                flag = 0
        return content_list, none_list