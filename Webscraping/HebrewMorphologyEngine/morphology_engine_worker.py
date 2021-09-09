import pika
import json
from Databases.DatabaseHandlers.queue_publisher import QueuePublisher
from Webscraping.HebrewMorphologyEngine.morphology_engine import HebrewMorphologyEngine
from Databases.DatabaseHandlers.cache_queue_publisher import CacheQueuePublisher


class MorphologyEngineWorker:
    def __init__(self, word_dict):
        connection_parameter = "localhost"
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.result = self.channel.queue_declare(queue="morphology_engine_queue", durable=True)
        self.word_dict = word_dict
        self.publisher = QueuePublisher("database")
        self.cache_publisher = CacheQueuePublisher()

    def morph(self, body, engine, id_number):
            text = body[id_number]
            text_list = text.split()
            base_words = []
            unmorphed_list = []
            for word in text_list:
                if word in self.word_dict.keys():
                    base_words.append(self.word_dict[word])
                else:
                    unmorphed_list.append(word)
            text = ' '.join(unmorphed_list)
            hebrew_morph_dict = engine.return_hebrew_morph_dict(text)
            for value in hebrew_morph_dict.values():
                base_words.append(value)
            full_text = ' '.join(base_words)
            for key, value in hebrew_morph_dict.items():
                self.cache_publisher.insert_data_to_queue(key, value)
            return full_text

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if type(body) == int:
            self.publisher.send_article_amount(body)
            return
        engine = HebrewMorphologyEngine()

        try:
            text = self.morph(body, engine, 2)
            morphed_title = self.morph(body, engine, 4)
            self.publisher.insert_morphed_data_to_queue(body[0], body[1], text, body[3], body[4], morphed_title)
            print("[+] Morphed text and title - {}".format(body[1]))

        except Exception as e:
            print(e)
            self.publisher.send_event_notification("Error in Parsing.")

    def start_consumption(self):
        self.channel.basic_consume(
            queue='morphology_engine_queue', on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()
