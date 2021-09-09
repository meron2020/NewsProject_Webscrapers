from Webscraping.Parsers.ynet_parser import YnetParser
from Webscraping.Parsers.maariv_parser import MaarivParser
from Webscraping.Parsers.N12_parser import N12Parser
from Webscraping.Parsers.walla_worker import WallaParser
import pika
from Databases.DatabaseHandlers.queue_publisher import QueuePublisher
import json
from Webscraping.Parsers.basic_worker import BasicParser


class QueueWorker:
    def __init__(self):
        self.morphology_queue_handler = QueuePublisher("morphology_engine_queue")

        self.news_links = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.result = self.channel.queue_declare(queue='url_queue', durable=True)

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if type(body) == int:
            self.morphology_queue_handler.send_article_amount(body)
            return

        topic = ''

        try:
            url, topic = body[0], body[1]
        except Exception:
            url = body[0]
        try:
            if "ynet" in url:
                worker = YnetParser(url)
                newspaper = "ynet"
            elif "maariv" in url:
                worker = MaarivParser(url)
                newspaper = "maariv"
            elif "mako" in url:
                worker = N12Parser(url)
                newspaper = "mako"
            else:
                worker = WallaParser(url)
                newspaper = "walla"
                topic = worker.topic_parse()
            full_text, title = worker.parse()
            full_text = ' '.join(full_text.split()[:50])
            title = BasicParser.remove_punctuation(title)
            self.morphology_queue_handler.insert_data_to_queue(newspaper, url, full_text, topic, title)
        #       worker.print_acknowledgement(newspaper)

        except Exception as e:
            print(e)
            self.morphology_queue_handler.send_event_notification("Error in Parsing.")
            # print(" [-] Error in parsing - {}".format(e))

    def start_consumption(self):
        self.channel.basic_consume(
            queue='url_queue', on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

# worker = QueueWorker()
# worker.start_consumption()
