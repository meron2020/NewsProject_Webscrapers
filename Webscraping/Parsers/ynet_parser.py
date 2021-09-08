from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class YnetParser(BasicParser):
    def __init__(self, url):
        super().__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        title_div = soup.find("div", {"class": "mainTitleWrapper"})
        h1_title = title_div.find("h1")
        title_text = h1_title.get_text()
        texts = []
        texts_span = soup.find_all("span", {"data-text": "true"})
        for span in texts_span:
            texts.append(span.getText())
        full_text = ''.join(texts)
        full_text = self.remove_punctuation(full_text)
        return full_text, title_text
