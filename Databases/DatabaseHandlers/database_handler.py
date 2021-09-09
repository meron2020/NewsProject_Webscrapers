import sqlite3
import pika
import json
import random
from Databases.DatabaseHandlers.queue_publisher import QueuePublisher
# from flask_app.Backend.Models.article import Article
# from flask_app.Backend.Models.score import Score
from ..PostgreSQL.postgresql_connection import PostgresConnection


class DatabaseHandler:
    def __init__(self):
        self.post_connection = PostgresConnection()
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue='database', durable=True)
        self.publisher = QueuePublisher("event_notifications")

        self.topic_dict = {}

        self.article_amount = 0
        self.articles_sent = 0

        self.articles_inserted_num = 0
        self.articles_not_inserted_num = 0

        self.create_topic_dict()

    def insert_article(self, newspaper, url, full_text, topic, title, morphed_title):
        if topic == "צבא ובטחון":
            topic = "צבא וביטחון"
        try:
            sqlite_query = PostgresConnection.create_article_insertion(newspaper, url, full_text, topic, title,
                                                                       morphed_title)
            self.post_connection.execute_query(sqlite_query)
            print("[+] Inserted Article")
            self.articles_inserted_num += 1
            if self.articles_inserted_num % 50 == 0:
                # print(" [+] {} articles inserted successfully.".format(self.find_articles_inserted_num()))
                # print(" [-] {} articles failed to insert.".format(self.articles_not_inserted_num))
                self.find_each_newspaper_num()

            if (self.articles_inserted_num + self.articles_not_inserted_num) == self.article_amount:
                self.find_each_newspaper_num()
                print("[+] Inserted {} articles out of {}".format(self.articles_inserted_num, self.article_amount))
                self.publisher.send_event_notification("Finished Webscraping")
        except sqlite3.Error as error:
            self.articles_not_inserted_num += 1
            print("Failed to insert data into sqlite table", error)
        return self.post_connection.cursor.lastrowid

    def insert_article_scores(self, first_id, second_id, first_title, second_title, title_score, text_score,
                              total_score):
        try:
            sqlite_query = PostgresConnection.create_score_insertion(first_id, second_id, first_title, second_title,
                                                                     title_score, text_score,
                                                                     total_score)
            self.post_connection.execute_query(sqlite_query)
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        return

    def find_articles_inserted_num(self):
        sqlite_query = """SELECT COUNT(*) FROM articles"""
        self.post_connection.execute_query(sqlite_query)
        articles_inserted = self.post_connection.curser_fetch_one()
        return articles_inserted

    def find_each_newspaper_num(self):
        newspaper_dict = {'ynet': 0, 'maariv': 0, 'walla': 0, 'mako': 0}
        cur_result = self.select_all_articles()
        for result in cur_result:
            for newspaper in newspaper_dict.keys():
                if newspaper in result[1]:
                    newspaper_dict[newspaper] += 1
        print("\n")
        for newspaper in newspaper_dict:
            print("{} - {}".format(newspaper, newspaper_dict[newspaper]))

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Error in Parsing.":
            self.articles_not_inserted_num += 1
            self.articles_sent += 1
        elif type(body) == int:
            self.article_amount = body
        else:
            _id = self.insert_article(body[0], body[1], body[2], body[3], body[4], body[5])
            # cluster_id = self.random_clustering(body[3])
            # self.update_cluster_id(_id, cluster_id)
            self.articles_sent += 1

    def start_consumption(self):
        self.channel.basic_consume(
            queue="database", on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

    def create_topic_dict(self):
        topic_dict = {'צבא וביטחון': [],
                      'מדיני': [],
                      'המערכת הפוליטית': [],
                      'פלסטינים': [],
                      'כללי': [],
                      'משפט ופלילים': [],
                      'חינוך ובריאות': [],
                      'חדשות בעולם': []}

        for topic in topic_dict.keys():
            topic_index = list(topic_dict.keys()).index(topic) * 4
            topic_dict[topic] = list(range(topic_index, topic_index + 4))

        self.topic_dict = topic_dict

    def update_cluster_id(self, _id, cluster_id):
        try:
            sqlite_query = """UPDATE articles SET cluster_id={} WHERE id={}""".format(cluster_id, _id)
            self.post_connection.execute_query(sqlite_query)
        except sqlite3.Error as error:
            print(" [-] Failed to insert cluster id.", error)

    def random_clustering(self, topic_arg):
        cluster_list = self.topic_dict[topic_arg]
        cluster_ids = []
        for i in range(2):
            cluster_ids.append(str(random.choice(cluster_list)))

        cluster_ids_str = ",".join(cluster_ids)
        return cluster_ids_str

    def select_all_articles(self):
        sqlite_query = """SELECT * FROM articles"""
        self.post_connection.execute_query(sqlite_query)
        articles = self.post_connection.curser_fetch_all()
        row_list = []
        for article in articles:
            row_list.append(article)

        return row_list

    def select_all_scores(self):
        sqlite_query = """SELECT * FROM score"""
        self.post_connection.execute_query(sqlite_query)
        scores = self.post_connection.curser_fetch_all()
        row_list = []
        for score in scores:
            row_list.append(score)
        return row_list

    def delete_all_rows(self):
        sqlite_query = """DELETE FROM articles"""
        self.post_connection.execute_query(sqlite_query)
        reset_sequence = """ALTER SEQUENCE articles_id_seq RESTART WITH 1;"""
        self.post_connection.execute_query(reset_sequence)

    def delete_all_score_rows(self):
        sqlite_query = """DELETE FROM score"""
        self.post_connection.execute_query(sqlite_query)

    def get_url_by_id(self, _id):
        url = self.post_connection.get_url_by_id(_id)
        return url
