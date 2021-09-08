import pika
import json


class QueuePublisher:
    def __init__(self, queue_name):
        connection_parameter = 'localhost'
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def insert_morphed_data_to_queue(self, newspaper, url, full_text, topic, title, morphed_title):
        payload = json.dumps([newspaper, url, full_text, topic, title, morphed_title])

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=payload
        )

    def insert_data_to_queue(self, newspaper, url, full_text, topic, title):
        payload = json.dumps([newspaper, url, full_text, topic, title])

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=payload
        )

    def send_event_notification(self, message):
        notification = json.dumps(message)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=notification
        )

    def send_article_amount(self, amount):
        self.amount = amount
        amount_json = json.dumps(amount)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=amount_json
        )
        # print("\n [x] Sent {} article to queue".format(newspaper))
