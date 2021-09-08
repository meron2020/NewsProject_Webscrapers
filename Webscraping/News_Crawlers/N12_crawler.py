from bs4 import BeautifulSoup
import requests
from .basic_crawler import BasicCrawler


class N12Crawler(BasicCrawler):
    def __init__(self):
        super(N12Crawler, self).__init__("https://www.n12.co.il/?partner=Newsheaderlogo")
        self.root_links = ["https://www.mako.co.il/news-military?partner=NewsNavBar",
                           "https://www.mako.co.il/news-politics?partner=NewsNavBar",
                           "https://www.mako.co.il/news-law?partner=NewsNavBar",
                           "https://www.mako.co.il/news-israel?partner=NewsNavBar",
                           "https://www.mako.co.il/news-lifestyle?partner=NewsNavBar",
                           "https://www.mako.co.il/news-education?partner=NewsNavBar"]
        self.topic_dict = {"military": 'צבא וביטחון', "politics": "המערכת הפוליטית", "law": "משפט ופלילים",
                           "israel": 'כללי',
                           "lifestyle": 'חינוך ובריאות', 'education': 'חינוך ובריאות'}
        self.news_links = []
        self.soup = BeautifulSoup(self.page_html, "html.parser")

    def find_news_links(self):
        for link in self.root_links:
            html = requests.get(link).text
            soup = BeautifulSoup(html, 'html.parser')
            figure_tags = soup.find("ul", {"class": "grid-ordering mainItem6"})
            counter = 0
            for tag in list(figure_tags.descendants):
                try:
                    link = tag.p.strong.a['href']
                    news_link = "https://www.mako.co.il" + link
                    for topic_key in self.topic_dict.keys():
                        if topic_key in news_link:
                            mako_article = [news_link, self.topic_dict[topic_key]]
                            if mako_article not in self.news_links:
                                self.news_links.append(mako_article)

                    counter += 1
                except Exception:
                    pass

        # print(self.news_links)
        # print(len(self.news_links))
        return self.news_links
