from scipy import spatial
import advertools as adv
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_app.Backend.Databases.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from flask_app.Backend.Webscraping.HebrewMorphologyEngine.morphology_engine import HebrewMorphologyEngine

hebrew_stoplist = adv.stopwords['hebrew']


class NLPProcessor:
    def __init__(self):
        self.terms = {}
        self.id_to_text_dict = {}
        self.id_to_tuple_dict = {}
        self.id_to_title_dict = {}
        self.morphology_engine = HebrewMorphologyEngine()
        self.handler = DatabaseHandlerOrchestrator()
        self.doc_idfs = {}
        self.full_texts_dict = {}
        self.used_urls = []
        self.used_titles = []
        self.tfidf_dict = {}

    def get_id_to_text_dict(self):
        rows_tuple_list = self.handler.get_all_rows_for_nlp()
        for row in rows_tuple_list:
            self.id_to_text_dict[str(row[0])] = row[3]
            self.id_to_tuple_dict[str(row[0])] = row
        return self.id_to_text_dict, self.id_to_tuple_dict

    def get_id_to_title_dict(self):
        for key, value in self.id_to_tuple_dict.items():
            self.id_to_title_dict[key] = value[6]

    @classmethod
    def find_cosine_similarity(cls, doc_1, doc_2):
        return 1 - spatial.distance.cosine(doc_1, doc_2)

    def return_texts(self):
        base_words_list = []
        for text in self.id_to_text_dict.values():
            base_words_list.append(text)
        return base_words_list

    def return_titles(self):
        title_list = []
        for title in self.id_to_title_dict.values():
            title_list.append(title)
        return title_list

    def get_url_from_id(self, _id):
        return self.id_to_tuple_dict[_id][1]

    def get_title_from_id(self, _id):
        return self.id_to_tuple_dict[_id][5]

    def sklearn_vectorize_texts(self):
        vectorizer = TfidfVectorizer(stop_words=hebrew_stoplist)
        vectors = vectorizer.fit_transform(self.return_texts())
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()

        return dense_list

    def sklearn_vectorize_title(self):
        vectorizer = TfidfVectorizer(stop_words=hebrew_stoplist)
        vectors = vectorizer.fit_transform(self.return_titles())
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()

        return dense_list

    @classmethod
    def turn_vectors_to_dict(cls, denseList):
        vector_dict = {}

        for vector in denseList:
            vector_dict[str(denseList.index(vector) + 1)] = vector

        cosine_similarity_dict = {}

        for _id, vector in vector_dict.items():
            vector_similarity_dict = {}
            for other_id, other_vector in vector_dict.items():
                similarity = NLPProcessor.find_cosine_similarity(vector, other_vector)
                if similarity != 1:
                    vector_similarity_dict[other_id] = similarity
            cosine_similarity_dict[_id] = vector_similarity_dict

        return cosine_similarity_dict

    @classmethod
    def find_top_similarities(cls, cosine_similarity_dict, minimum_similarity):
        top_similarities_dict = {}
        for _id, vector_similarity_dict in cosine_similarity_dict.items():
            top_dict = {}
            for other_id, similarity in vector_similarity_dict.items():
                if similarity > minimum_similarity:
                    top_dict[other_id] = similarity
            top_similarities_dict[_id] = top_dict

        return top_similarities_dict

    def get_url_dict(self, top_similarities_dict):
        used_urls = []
        urls_dict = {}
        for _id, top_four_dict in top_similarities_dict.items():
            top_four_url_dict = {}
            try:
                for inner_id in top_four_dict.keys():
                    url = self.get_url_from_id(inner_id)
                    if url not in used_urls:
                        top_four_url_dict[inner_id] = [url, format(top_four_dict[inner_id], ".3f")]
                urls_dict[_id] = top_four_url_dict
            except Exception as e:
                urls_dict[_id] = {}
        return urls_dict

    def get_title_similars(self, top_similarities_dict):
        used_titles = []
        titles_dict = {}
        for _id, top_dict in top_similarities_dict.items():
            top_title_dict = {}
            try:
                for inner_id in top_dict.keys():
                    title = self.get_title_from_id(inner_id)
                    if title not in used_titles:
                        top_title_dict[inner_id] = [title, format(top_dict[inner_id], ".3f")]
                titles_dict[_id] = top_title_dict
            except Exception as e:
                titles_dict[_id] = {}
        return titles_dict

    def present_urls_similars(self, urls_dict):
        for _id, url_dict in urls_dict.items():
            base_url = self.get_url_from_id(_id)
            if base_url not in self.used_urls:
                print(base_url + "  >>")
                url_list = []
                try:
                    for url in url_dict.values():
                        if base_url not in self.used_urls:
                            if len(url) == 0:
                                print("No similar texts")
                            else:
                                url_list.append(url)
                                self.used_urls.append(url)
                except Exception:
                    print("No similar texts")

                print(url_list)
                print("\n")

    def present_titles_similars(self, title_dict):
        for _id, title_dict in title_dict.items():
            base_title = self.get_title_from_id(_id)
            if base_title not in self.used_titles:
                print(base_title + "  >>")
                title_list = []
                try:
                    for url in title_dict.values():
                        if base_title not in self.used_titles:
                            if len(url) == 0:
                                print("No similar texts")
                            else:
                                title_list.append(url)
                                self.used_titles.append(url)
                except Exception:
                    print("No similar texts")

                print(title_list)
                print("\n")

    print("\n")

    def get_average_similarity(self, titles_similarities, texts_similarities, graph):
        articles_dict = self.handler.get_all_rows_for_graph()
        for _id in titles_similarities.keys():
            graph.add_node(_id)
        for _id, similar_articles in titles_similarities.items():
            new_id_score_dict = {}
            first_title = articles_dict[int(_id)][4]
            for other_id, score in similar_articles.items():
                second_title = articles_dict[int(other_id)][4]
                try:
                    title_score = score * 0.7
                    text_score = texts_similarities[_id][other_id] * 0.3
                    score = title_score + text_score
                except KeyError:
                    score = score * 0.7
                    title_score = score
                    text_score = 0
                self.handler.insert_scores(int(_id), int(other_id), first_title, second_title, title_score, text_score,
                                           score)
                if score > 0.12:
                    graph.add_edge(_id, other_id)
                    print("Added Node")
        return graph


if __name__ == "__main__":
    processor = NLPProcessor()
    processor.get_id_to_text_dict()
    processor.get_id_to_title_dict()
    texts_dense_list = processor.sklearn_vectorize_texts()
    texts_similarity_dict = NLPProcessor.turn_vectors_to_dict(texts_dense_list)
    texts_top_similarities = NLPProcessor.find_top_similarities(texts_similarity_dict, 0.175)
    # processor.present_urls_similars(texts_url_dict)
    title_dense_list = processor.sklearn_vectorize_title()
    title_similarity_dict = NLPProcessor.turn_vectors_to_dict(title_dense_list)
    title_top_similarities = NLPProcessor.find_top_similarities(title_similarity_dict, 0.175)
    average_score_dict = processor.get_average_similarity(title_top_similarities, texts_top_similarities)
    titles_dict = processor.get_title_similars(average_score_dict)
    processor.present_titles_similars(titles_dict)
