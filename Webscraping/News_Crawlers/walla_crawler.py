import requests
from bs4 import BeautifulSoup
from .basic_crawler import BasicCrawler


class WallaCrawler(BasicCrawler):
    def __init__(self):
        super(WallaCrawler, self).__init__("https://news.walla.co.il/")
        self.root_links = ["https://news.walla.co.il/category/12837",
                           "https://news.walla.co.il/category/2689",
                           "https://news.walla.co.il/category/1",
                           "https://news.walla.co.il/category/2686",
                           "https://news.walla.co.il/category/2"]

        self.news_links = []

    def find_all_links(self):
        html = requests.get("https://news.walla.co.il/").text
        soup = BeautifulSoup(html, 'html.parser')
        css_divs = soup.body.find_all("div", {"class": 'css-ev747'})
        not_used_categories = ['מדע וסביבה', 'אסור לפספס', 'דעות ופרשנויות']
        all_links = []
        for css_div in css_divs:
            if css_div.find("h2").get_text() not in not_used_categories:
                events_div = css_div.find("div", {"class": 'events'})
                for link in events_div.find_all("a"):
                    all_links.append([link['href']])

        return all_links
