import psycopg2
from psycopg2 import Error


class PostgresConnection:
    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="yoav",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="articles")
        self.cursor = self.connection.cursor()

    def execute_query(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.connection.rollback()

    @classmethod
    def create_article_insertion(cls, newspaper, url, full_text, topic, title, morphed_title):
        newspaper = "'" + newspaper + "'"
        url = "'" + url + "'"
        full_text = "'" + full_text + "'"
        topic = "'" + topic + "'"
        title = "'" + title + "'"
        morphed_title = "'" + morphed_title + "'"
        insert_query = """INSERT INTO public.articles (newspaper, url, full_text, topic, title, morphed_title, cluster_id) 
        VALUES ({}, {}, {}, {}, {}, {}, NULL)""".format(newspaper, url, full_text, topic, title, morphed_title)
        return insert_query

    @classmethod
    def create_morphed_insertion(cls, word, morphed_word):
        word = word.replace("'", "")
        morphed_word = morphed_word.replace("'", "")
        word = "'" + word + "'"
        morphed_word = "'" + morphed_word + "'"
        insert_query = """INSERT INTO morphed (word, morphed_word) VALUES ({}, {})""".format(word, morphed_word)
        return insert_query

    @classmethod
    def create_score_insertion(cls, first_id, second_id, first_title, second_title, title_score, text_score,
                               total_score):
        first_title = "'" + first_title + "'"
        second_title = "'" + second_title + "'"
        insert_query = """INSERT INTO score (first_id, second_id, first_title, second_title, title_score, text_score,
                          total_score) VALUES ({}, {}, {}, {}, {}, {}, {})""".format(first_id, second_id, first_title,
                                                                                     second_title, title_score,
                                                                                     text_score,
                                                                                     total_score)
        return insert_query

    def get_cursor(self):
        return self.cursor

    def curser_fetch_all(self):
        return self.cursor.fetchall()

    def curser_fetch_one(self):
        return self.cursor.fetchone()

    def select_all_topic_rows(self, topic):
        topic = "'" + topic + "'"
        sqlite_query = """SELECT * FROM articles WHERE topic={}""".format(topic)
        self.execute_query(sqlite_query)
        rows = self.cursor.fetchall()
        return rows

    def get_url_by_id(self, _id):
        sqlite_query = """SELECT url FROM articles WHERE id={}""".format(_id)
        self.execute_query(sqlite_query)
        url = self.cursor.fetchall()
        return url
