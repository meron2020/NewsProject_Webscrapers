from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class WallaParser(BasicParser):
    def __init__(self, url):
        super(WallaParser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        header_div = soup.find("section", {"class": "item-main-content"})
        header_div = header_div.find("header")
        h1_title = header_div.find("h1")
        title_text = h1_title.get_text()
        text_div = soup.find("section", {"class": "article-content"})
        full_text = text_div.get_text()
        full_text = self.remove_punctuation(full_text)
        return full_text, title_text

    def topic_parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        nav_ul = soup.find("article", {"class": "common-item"}).find("nav").find("ul")
        if nav_ul.find_all("li")[-2].a['title'] == "חדשות בעולם":
            topic = 'חדשות בעולם'
            return topic
        topic = nav_ul.find_all("li")[-1].a['title']
        if topic == 'קורונה':
            topic = "חינוך ובריאות"
        elif topic == 'פוליטי-מדיני':
            topic = 'מדיני'
        elif topic == 'יחסי חוץ':
            topic = 'מדיני'
        elif topic == 'חדשות פלילים ומשפט':
            topic = 'משפט ופלילים'
        elif topic == 'אירועים בארץ':
            topic = 'כללי'
        return topic
