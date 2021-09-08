from bs4 import BeautifulSoup
from .basic_crawler import BasicCrawler


class MaarivCrawler(BasicCrawler):
    def __init__(self):
        super(MaarivCrawler, self).__init__("https://www.maariv.co.il/news")
        self.no_topic_news_links = []
        self.soup = BeautifulSoup(self.page_html, "html.parser")
        self.topic_dict = {"politics": 'המערכת הפוליטית', "military": 'צבא וביטחון', "world": 'חדשות בעולם',
                           "health": 'בריאות',
                           "law": 'משפט ופלילים', "Education": 'חינוך', "israel": 'כללי'}

        self.news_links = []

    def find_big_item_links(self):
        news_links = []
        big_items_list = self.soup.find_all("div", {"class": "category-five-articles-big-item"})

        for i in range(len(big_items_list)):
            news_link = big_items_list[i].a['href']
            news_links.append(news_link)

        return news_links

    def find_small_item_links(self):
        news_links = []
        small_items_list = self.soup.find_all("div", {"class": "category-five-articles-small-item"})
        for small_item in small_items_list:
            news_link = small_item.a['href']
            news_links.append(news_link)
        return news_links

    def return_news_links(self):
        big_links = self.find_big_item_links()
        small_links = self.find_small_item_links()
        self.no_topic_news_links.extend(big_links)
        self.no_topic_news_links.extend(small_links)

        for link in self.no_topic_news_links:
            for topic_key in self.topic_dict.keys():
                if topic_key in link:
                    if topic_key == "Education" or topic_key == "health":
                        self.news_links.append([link, 'חינוך ובריאות'])
                    else:
                        self.news_links.append([link, self.topic_dict[topic_key]])
        return self.news_links
