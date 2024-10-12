import pickle
import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from text_processing import TextProcessing


class MatchingRanking:
    @classmethod
    def search(cls, dataset: str, query: str, count=10):
        if dataset == "wikir":
            vectorizer = wikir_vectorizer
            tfidf_matrix = wikir_tfidf_matrix
            corpus = wikir_corpus
        elif dataset == "antique":
            vectorizer = antique_vectorizer
            tfidf_matrix = antique_tfidf_matrix
            corpus = antique_corpus
        else:
            raise NameError("Dataset must be wikir or antique")

        # Transform query to VSM
        query = [query]
        queryVector = vectorizer.transform(query)

        # Calculate cosine similarity
        cosine_scores = cosine_similarity(queryVector, tfidf_matrix)

        # Get the indices of the documents sorted by their cosine similarity score in descending order
        sorted_indices = np.argsort(cosine_scores.flatten())[::-1]

        # Create a list of corpus keys
        keys_list = list(corpus.keys())

        # Return the top [count] relevant documents
        docs = {}
        for idx in sorted_indices[:count]:
            # Check if the cosine score is zero
            if cosine_scores[0][idx] == 0: break

            doc_id = keys_list[idx]
            docs[doc_id] = corpus[doc_id]
        
        return docs

    @classmethod
    def load_index(cls, dataset, version="00"):
        with open(f'Datasets/{dataset}/index/vectorizer{version}.pickle', 'rb') as f:
            vectorizer = pickle.load(f)

        tfidf_matrix = load_npz(f'Datasets/{dataset}/index/index{version}.npz')
        return tfidf_matrix, vectorizer


# Load indices and models
wikir_tfidf_matrix, wikir_vectorizer = MatchingRanking.load_index("wikIR1k", "01")
antique_tfidf_matrix, antique_vectorizer = MatchingRanking.load_index("antique", "02")


# Load datasets
df = pd.read_csv('Datasets/wikIR1k/documents.csv')
wikir_corpus = df.set_index('id_right')['text_right'].to_dict()

antique_corpus = {}
with open("Datasets/antique/antique-collection.txt", 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            identifier, text = line.split('\t', 1)
            antique_corpus[identifier] = text
