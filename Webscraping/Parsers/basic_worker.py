import requests
from string import punctuation

class BasicParser:
    def __init__(self, url):
        self.url = url
        self.page_html = self.download_link()

    def download_link(self):
        r = requests.get(self.url)
        return r.text

    @classmethod
    def remove_punctuation(cls, text):
        text = text.replace("'", "")
        text = text.replace('"', "")
        for punc in punctuation:
            text = text.replace(punc, " ")

        return text


    # @classmethod
    # def print_acknowledgement(cls, newspapaer):
    #     print(" [x] {} url received.".format(newspapaer))
