from bs4 import BeautifulSoup
from .basic_crawler import BasicCrawler


class IsraelHayomCrawler(BasicCrawler):
    def __init__(self):
        super(IsraelHayomCrawler, self).__init__("https://www.israelhayom.co.il/news")
        self.soup = BeautifulSoup(self.page_html, "html.parser")
        self.topic_dict = {"defense": 'צבא וביטחון', "world-news": "חדשות בעולם", "geopolitics": "חדשות בעולם",
                           "politics": 'המערכת הפוליטית', "local": "כללי", "crime": 'משפט ופלילים'}

    def parse_and_download(self):
        articles_div = self.soup.body.find_all("a")
        article_types = ['politics', 'defense', 'geopolitics', 'world-news', 'local', 'crime']
        article_links = []
        for article in articles_div:
            for article_type in article_types:
                if article_type in article['href']:
                    article_link = "https://www.israelhayom.co.il/" + article['href']
                    article_links.append([article_link, self.topic_dict[article_type]])

        # print(article_links)
        # print(len(article_links))
        return article_links


# crawler = IsraelHayomCrawler()
# crawler.parse_and_download()
