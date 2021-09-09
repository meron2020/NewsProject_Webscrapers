from Databases.DatabaseHandlers.database_handler import DatabaseHandler
import sqlite3
from Databases.DatabaseHandlers.cache_database_handler import CacheDatabaseHandler


class DatabaseHandlerOrchestrator:
    def __init__(self):
        self.handler = DatabaseHandler()
        self.cache_handler = CacheDatabaseHandler()

    def run_orchestrator(self):
        self.handler.delete_all_rows()
        print("Successfully deleted all rows in articles table")
        self.handler.start_consumption()

    def create_score_db(self):
        try:
            self.handler.delete_all_score_rows()
        except sqlite3.OperationalError:
            pass
        self.handler.delete_all_score_rows()
        print("Successfully deleted all rows in scores table")

    def update_cluster_ids(self, cluster_ids_dict):
        for cluster_id, articles in cluster_ids_dict.items():
            for article in articles:
                self.handler.update_cluster_id(article, cluster_id)

    def create_cache_db(self):
        print("Successfully Connected to morph_cache DB Table")
        self.cache_handler.start_consumption()

    def get_all_rows_from_cache(self):
        return self.cache_handler.return_word_to_morph_dict()

    def get_all_rows(self):
        print("Successfully Connected to SQLite")
        return self.handler.select_all_articles()

    def get_all_rows_for_graph(self):
        print("Successfully Connected to SQLite")
        rows = self.handler.select_all_articles()
        rows_dict = {}
        for row in rows:
            rows_dict[row[0]] = row
        return rows_dict

    def get_all_rows_from_scores(self):
        return self.handler.select_all_scores()

    def get_all_rows_for_nlp(self):
        print("Successfully Connected to SQLite")
        return self.handler.select_all_articles()

    def insert_scores(self, first_id, second_id, first_title, second_title, title_score, text_score, total_score):
        self.handler.insert_article_scores(first_id, second_id, first_title, second_title, title_score, text_score,
                                           total_score)

    def delete_all_rows_in_scores(self):
        self.handler.delete_all_score_rows()

    def get_url_by_id(self, _id):
        return self.handler.get_url_by_id(_id)
