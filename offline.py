import pickle
import pandas as pd

from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize

from text_processing import TextProcessing

class Indexing:
    @classmethod
    def generate_index(cls, dataset_path: str, dataset_name: str, version="00"):
        corpus = {}

        # Load dataset
        if dataset_path.endswith("csv"):
            df = pd.read_csv(dataset_path)
            corpus = df.set_index('id_right')['text_right'].to_dict()
            
        elif dataset_path.endswith("txt"):
            with open(dataset_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        identifier, text = line.split('\t', 1)
                        corpus[identifier] = text

        # Create VSM Index
        vectorizer = TfidfVectorizer(preprocessor=TextProcessing.process, tokenizer=word_tokenize)
        tfidf_matrix = vectorizer.fit_transform(corpus.values())
        
        # Save index as file
        save_npz(f'Datasets/{dataset_name}/index/index{version}.npz', tfidf_matrix)
        
        # Save model as file
        with open(f'Datasets/{dataset_name}/index/vectorizer{version}.pickle', 'wb') as f:
            pickle.dump(vectorizer, f)
            

Indexing.generate_index("Datasets/wikIR1k/documents.csv", "wikIR1k", version="05")