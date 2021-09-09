import json
import threading

import plotly.graph_objects as go
import networkx as nx
import networkx.algorithms.components as nac
from googleapiclient import discovery

from Clustering.NLP.nlp_algorithms import NLPProcessor
from Databases.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
import pika
import pandas as pd


class GraphConnections:
    def __init__(self):
        self.handler = DatabaseHandlerOrchestrator()
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue="event_notifications", durable=True)
        self.processor = ""
        self.id_to_text_dict = ""
        self.id_to_tuple_dict = ""
        self.finished_clustering = False

    def create_NLP(self):
        self.processor = NLPProcessor()
        self.id_to_text_dict, self.id_to_tuple_dict = self.processor.get_id_to_text_dict()
        self.processor.get_id_to_title_dict()

    def find_top_similarities(self):
        texts_dense_list = self.processor.sklearn_vectorize_texts()
        texts_similarity_dict = NLPProcessor.turn_vectors_to_dict(texts_dense_list)
        texts_top_similarities = NLPProcessor.find_top_similarities(texts_similarity_dict, 0.175)
        title_dense_list = self.processor.sklearn_vectorize_title()
        title_similarity_dict = NLPProcessor.turn_vectors_to_dict(title_dense_list)
        title_top_similarities = NLPProcessor.find_top_similarities(title_similarity_dict, 0.125)
        return texts_top_similarities, title_top_similarities

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Finished Webscraping":
            compute = discovery.build('compute', 'v1')
            request = compute.instances().stop(project="sonic-shuttle-322109", zone="europe-west6-a",
                                               instance="instance-1")
            request.execute()
            self.create_NLP()
            nx_graph = self.create_graph()
            self.update_cluster_ids(nx_graph)
        return

    def create_graph(self):
        G = nx.Graph()
        texts_top_similarities, title_top_similarities = self.find_top_similarities()
        graph = self.processor.get_average_similarity(title_top_similarities, texts_top_similarities, G)
        return graph

    def update_cluster_ids(self, nx_graph):
        cluster_id_dict = {}
        cluster_number = 0
        for cluster_set in (nac.connected_components(nx_graph)):
            cluster_id_dict[cluster_number] = cluster_set
            cluster_number += 1
        self.handler.update_cluster_ids(cluster_id_dict)

    def get_url_to_url_score(self):
        url_to_url_score = {
            # "first_url": [],
            # "second_url": [],
            "first_title": [],
            "second_title": [],
            "title_score": [],
            "text_score": [],
            "score": []
        }
        article_dict = self.handler.get_all_rows_for_graph()
        for score_row in self.handler.get_all_rows_from_scores():
            first_url = article_dict[score_row[0]][1]
            second_url = article_dict[score_row[1]][1]
            first_title = article_dict[score_row[0]][5]
            second_title = article_dict[score_row[1]][5]
            # url_to_url_score["first_url"].append(first_url)
            # url_to_url_score["second_url"].append(second_url)
            url_to_url_score["first_title"].append(first_title)
            url_to_url_score["second_title"].append(second_title)
            url_to_url_score["title_score"].append(score_row[4])
            url_to_url_score["text_score"].append(score_row[5])
            url_to_url_score["score"].append(score_row[6])
        return url_to_url_score

    def show_df_url_to_url(self):
        url_to_url_score = self.get_url_to_url_score()
        df = pd.DataFrame(url_to_url_score)
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[
                # df.first_url, df.second_url,
                df.first_title,
                df.second_title, df.title_score, df.text_score, df.score],
                fill_color='lavender',
                align='right',
                font_size=14,
                height=30
            ))
        ])

        fig.show()

    def start_consumption(self):
        self.channel.basic_consume(
            queue="event_notifications", on_message_callback=self.callback, auto_ack=True
        )
        self.channel.start_consuming()
        return


if __name__ == "__main__":
    graph_connections = GraphConnections()
    graph_connections.create_NLP()
    nx_graph = graph_connections.create_graph()
    graph_connections.update_cluster_ids(nx_graph)
    # graph_connections.show_df_url_to_url()
