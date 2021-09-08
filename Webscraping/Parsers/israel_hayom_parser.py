from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class IsraelHayomParser(BasicParser):
    def __init__(self, url):
        super(IsraelHayomParser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        text_div = soup.find("div", {"class": "text-content"})
        return text_div.get_text()
