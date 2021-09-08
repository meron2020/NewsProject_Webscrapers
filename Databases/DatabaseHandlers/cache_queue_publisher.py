import json
import pika


class CacheQueuePublisher:
    def __init__(self):
        connection_parameter = 'localhost'
        self.queue_name = "morphology_cache"
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def insert_data_to_queue(self, word, morphed_word):
        payload = json.dumps([word, morphed_word])

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=payload
        )
