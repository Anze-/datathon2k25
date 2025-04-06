import faiss
import pickle
from embedder import get_embedding
from config import INDEX_PATH, DOCS_PATH
import numpy as np


def build_index(documents: list[str]):
    vectors = [get_embedding(doc) for doc in documents]
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype("float32"))

    # Save index
    faiss.write_index(index, INDEX_PATH)

    # Save documents
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(documents, f)


def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)
    return index, documents
