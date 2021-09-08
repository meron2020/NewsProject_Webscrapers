import requests


class BasicCrawler:
    def __init__(self, url):
        self.root_links = []
        self.page_html = self.get_link(url)

    @classmethod
    def get_link(cls, url):
        r = requests.get(url)
        return r.text

    def check_if_links_change(self, find_news_links):
        news_links = find_news_links()
        if not news_links == self.root_links:
            self.root_links = news_links

        else:
            pass
