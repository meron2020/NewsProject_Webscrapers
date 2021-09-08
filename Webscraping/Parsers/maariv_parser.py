from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class MaarivParser(BasicParser):
    def __init__(self, url):
        super(MaarivParser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        title_div = soup.find("div", {"class": "article-title"})
        h1_title = title_div.find("h1")
        title_text = h1_title.get_text()
        title_text.replace('"', "'")
        texts = []
        full_text = ""
        texts_div = soup.find_all("div", {"class": "article-body"})
        for text_p in texts_div:
            texts.append(text_p.find_all('p'))

        for text in texts[0]:
            full_text += text.get_text()

        full_text_list = full_text.split()
        for text in full_text_list:
            text = text[::-1]
        full_text = ' '.join(full_text_list)

        full_text = self.remove_punctuation(full_text)
        return full_text, title_text
