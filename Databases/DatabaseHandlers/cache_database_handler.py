import json
import sqlite3
import pika
from ..PostgreSQL.postgresql_connection import PostgresConnection


class CacheDatabaseHandler:
    def __init__(self):
        self.post_connection = PostgresConnection()
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue='morphology_cache', durable=True)

    def insert_morphology_words(self, word, morphed_word):
        try:
            sqlite_query = self.post_connection.create_morphed_insertion(word, morphed_word)
            self.post_connection.execute_query(sqlite_query)
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def return_word_to_morph_dict(self):
        sqlite_query = """SELECT * FROM morphed"""
        self.post_connection.execute_query(sqlite_query)
        morphed_words = self.post_connection.curser_fetch_all()
        morphology_cache = {}
        for morphed in morphed_words:
            morphology_cache[morphed[0]] = morphed[1]
        return morphology_cache

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        self.insert_morphology_words(body[0], body[1])

    def start_consumption(self):
        self.channel.basic_consume(
            queue="morphology_cache", on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()
