from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class N12Parser(BasicParser):
    def __init__(self, url):
        super(N12Parser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        title_h1 = soup.find("h1")
        title_text = title_h1.get_text()
        full_text = ""
        text_divs = soup.find_all("p")
        text_divs.pop()
        for text_div in text_divs:
            full_text += text_div.get_text()

        full_text = self.remove_punctuation(full_text)
        return full_text, title_text


