from flask_app.Backend.Webscraping.News_Crawlers.CrawlersHandler import CrawlersHandler


class TestingUrlsSender:
    @classmethod
    def send_urls(cls):
        url =[["https://www.ynet.co.il/news/article/byeya7xxy#autoplay", "צבא וביטחון"]]
        urls = [
            ["https://www.ynet.co.il/news/article/byeya7xxy#autoplay", "צבא וביטחון"],
            ["https://www.ynet.co.il/news/article/r1dfhexlf#autoplay", "חינוך ובריאות"],
            ["https://www.ynet.co.il/news/article/bkjuhtjgk#autoplay", "מדיני"],
            ["https://www.ynet.co.il/news/article/hyp006ojly", "צבא וביטחון"],
            ["https://www.ynet.co.il/news/article/s1yxnocjf#autoplay", "המערכת הפוליטית"],
            ["https://www.ynet.co.il/news/article/h1ji87lgf#autoplay", "חדשות בעולם"],
            ["https://www.ynet.co.il/news/article/s1zojl1xy", "המערכת הפוליטית"],
            ["https://news.walla.co.il/item/3453301", "חדשות בעולם"],
            ["https://news.walla.co.il/item/3453248"],
            ["https://news.walla.co.il/break/3453484"],
            ["https://www.maariv.co.il/news/military/Article-858557", "צבא וביטחון"],
            ["https://www.maariv.co.il/news/military/Article-858551", "צבא וביטחון"],
            ["https://www.maariv.co.il/news/world/Article-858553", "חדשות בעולם"],
            ["https://www.mako.co.il/news-military/2021_q3/Article-d8b08da5d8e2b71026.htm?partner=lobby", "צבא וביטחון"],
            ["https://www.mako.co.il/news-military/2021_q3/Article-68a72e5a92b1b71027.htm", "צבא וביטחון"],
            ["https://www.n12.co.il/news-lifestyle/2021_q3/Article-3fece949d703b71026.htm?sCh=31750a2610f26110&pId=173113802", "חינוך ובריאות"],
            ["https://www.mako.co.il/news-politics/2021_q3/Article-a3a1416948c2b71027.htm?partner=lobby", "המערכת הפוליטית"]
        ]

        handler = CrawlersHandler()
        handler.send_test_urls_to_queue(url)
