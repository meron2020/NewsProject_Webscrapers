from .ynet_crawler import YnetCrawler
from .maariv_crawler import MaarivCrawler
from .N12_crawler import N12Crawler
from .walla_crawler import WallaCrawler
import pika
import json


class CrawlersHandler:
    def __init__(self):
        connection_parameter = 'localhost'
        self.ynet_crawler = YnetCrawler()
        self.maariv_crawler = MaarivCrawler()
        self.n12_crawler = N12Crawler()
        self.walla_crawler = WallaCrawler()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="url_queue", durable=True)
        self.news_links = []

    def crawl_links(self):
        self.find_all_news_links()
        self.send_article_amount()
        self.send_links_to_queue()

        self.connection.close()
        # self.send_one_link_to_queue()
        print("We have " + str(len(self.news_links)) + " articles")

    def send_article_amount(self):
        amount = json.dumps(len(self.news_links))
        self.channel.basic_publish(
            exchange='',
            routing_key='url_queue',
            body=amount
        )
        print(" [x] Sent article amount to queue.")

    def send_link_to_queue(self, link):
        link = json.dumps(link)
        self.channel.basic_publish(
            exchange='',
            routing_key='url_queue',
            body=link
        )
        print(" [x] Sent {} to queue".format(link))

    def send_links_to_queue(self):
        for link in self.news_links:
            self.send_link_to_queue(link)

    def send_num_of_links_to_queue(self):
        for i in range(10):
            self.send_link_to_queue(self.news_links[i])
        self.connection.close()

    def find_all_news_links(self):
        ynet_links = self.ynet_crawler.find_all_links()
        self.news_links.extend(ynet_links)
        maariv_links = self.maariv_crawler.return_news_links()
        self.news_links.extend(maariv_links)
        walla_links = self.walla_crawler.find_all_links()
        self.news_links.extend(walla_links)
        n12_links = self.n12_crawler.find_news_links()
        self.news_links.extend(n12_links)

    def send_test_urls_to_queue(self, urls_list):
        for url in urls_list:
            self.send_link_to_queue(url)

# handler = CrawlersHandler()
# handler.crawlLinks()
