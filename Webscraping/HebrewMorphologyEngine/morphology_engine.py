import requests
import string

string_letters = string.ascii_letters
string_upper = string.ascii_uppercase


class HebrewMorphologyEngine:
    def __init__(self):
        self.ip = "http://34.65.165.8:8000/yap/heb/joint"

    def return_hebrew_morph_dict(self, text):
        data = '{"text": "' + text + '  "}'
        response = requests.get(self.ip,
                                data=data.encode(
                                    "utf-8"),
                                headers={
                                    "Content-Type": "application/json"
                                },
                                cookies={},
                                auth=(),
                                )

        text_list = text.split()
        split_response = response.json()['md_lattice'].split("\n")
        hebrew_words_dict = {}
        one_word_before = False
        for category in split_response:
            word_list = category.split()
            try:
                if len(word_list[2]) != 1:
                    if one_word_before:
                        for full_word in text_list:
                            if word_list[2] in full_word:
                                hebrew_words_dict[full_word] = word_list[3]
                        one_word_before = False
                    else:
                        hebrew_words_dict[word_list[2]] = word_list[3]
                else:
                    one_word_before = True
            except Exception:
                pass
        return hebrew_words_dict
