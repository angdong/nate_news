import requests 
import datetime as dt
from bs4 import BeautifulSoup as bs

LINK = 'https://news.nate.com/view/'

# TODO: return DataFrame form news
# TODO: Real-time crawl(with same domain)
# TODO: find "similar" news
"""
    1. same category
    2. same contents(search..?)
    3. same press
    4. etc.
"""

class NateNews:    
    """Crawler for natenews
    
    Args:
        `url` (str): news url, form should be https://news.nate.com/view/{DATE}n{ARTICLE_NUM}
    
    Var:
        `self.url`: article's url
        `self.content`: article content
    """    
    def __init__(self, url:str):
        res = requests.get(url)
        assert res.status_code == 200
        
        self.url = url
        html = res.text
        self.content = bs(html, 'html.parser')

        # TODO: will be used (self.day, self.post_num)
        # self.day = int(url.split('/')[-1].split('n'))
        # self.post_num = int(url.split('/')[-1].split('n'))
    
    def get_info(self):
        """get information of `NateNews`
        
        Desc:
            1. title
            2. category
            3. press
            4. date
            5. content
            6. url

        Returns:
            List[str]: information of `NateNews`
        """
        return[
            self._get_title(),
            self._get_category(),
            self._get_press(),
            self._get_date(),
            self._get_content(),
            self.url
        ]

    # @property
    # def press(self):
    #     return self._get_press()
    
    # @property
    # def category(self):
    #     return self._get_category()

    def _get_press(self):
        # TODO: get hyperlink of same press

        press = self.content.find('a', {'class': 'medium'})
        return press.text

    def _get_category(self):
        nav = self.content.find('div', {'id': 'mediaSubnav'})
        category = nav.find('h3')
        return category.text

    def _get_content(self):
        # TODO: data cleaning
        # TODO: accumulate all the attributes below
        article = self.content.find('div', {'id': 'realArtcContents'})
        text = article.text

        return text
    
    def _get_title(self):
        title = self.content.find('h3', {'class': 'articleSubecjt'})
        return title.text
    
    
    def _get_date(self):
        # TODO: get article of same date
        
        _date = self.content.find('span', {'class': 'firstDate'})
        date = _date.find('em').text
        # time = dt.datetime.strptime(_time, "%Y-%m-%d %H:%M")
        return date
    
    
    @staticmethod
    def get_recent(date: int):
        """get latest article number in Nate given date

        Args:
            `date` (int): date in which latest article number will be found

        Note:
            Can't return accurate number of article
            -> get latest number of article in '최신뉴스' in Nate

        Returns:
            int: latest article number
        """        
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
        """create `NateNews` if it satisfy some conditions

        Args:
            `url` (str): url for news in Nate

        Desc:
            return `NateNews` if given url satisfy some conditions
            * 1. Should have article(RealArtcContents or articleContetns)
            * 2. Only for '뉴스', exclude for '연예', '스포츠'
            
        Returns:
            Union[NateNews, None]: 
        """        
        # TODO: add exclusion rule for press('연합뉴스',etc..)
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
        else:
            return new_class
        
        # code for check '뉴스', '연예', '스포츠'
        # which_news = new_class.content.find(
        #     'a',
        #     {'class': 'svcname'}
        # ).text
        # if which_news == '뉴스':
        #     return new_class
        # else:
        #     return None
