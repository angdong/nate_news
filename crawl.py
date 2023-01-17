import requests
import datetime as dt
from bs4 import BeautifulSoup as bs


class NateNews:
    """
    Docstring
    """
    def __init__(self, url:str):
        res = requests.get(url)
        assert res.status_code == 200
        
        html = res.text
        self.content = bs(html, 'html.parser')

    def get_contents(self):
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
    
    def _get_date(self):
        # TODO: get article of same date
        
        _date = self.content.find('span', {'class': 'firstDate'})
        _date = _date.find('em').text
        date = dt.datetime.strptime(_date, "%Y-%m-%d %H:%M")
        return date.text
    
    def get_press(self):
        # TODO: get hyperlink of same press

        press = self.content.find('a', {'class': 'medium'})
        return press.text