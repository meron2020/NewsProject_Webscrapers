from bs4 import BeautifulSoup
import pika
from basic_crawler import BasicCrawler


class HaaretzCrawler(BasicCrawler):
    def __init__(self):
        super().__init__("https://www.haaretz.co.il/")
        self.news_links = []
        self.send_links_to_queue(self.news_links)

    def find_all_news_links(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        article_tags = soup.find_all("article")
        for article in article_tags:
            try:
                article_link = article.a['href']
                if "news" in article_link or "health" in article_link:
                    if "https" not in article_link:
                        news_link = "https://www.haaretz.co.il/" + article_link
                        self.news_links.append(news_link)

            except Exception:
                pass

        print(self.news_links)


crawler = HaaretzCrawler()
crawler.find_all_news_links()
