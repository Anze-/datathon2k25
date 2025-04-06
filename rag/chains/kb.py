from __future__ import annotations

from datetime import time
from typing import List
from owlready2 import get_ontology

import warnings

from sentence_transformers import SentenceTransformer

import config
import torch

warnings.filterwarnings("ignore")

sentence_transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def calculate_similarity(query: str, entities) -> List[float]:
    """Calculate semantic similarity between the user query and RDF entities"""
    print("Query", query)
    query_embedding = sentence_transformer.encode([query], show_progress_bar=True)
    print("Embedded query!")
    entity_embeddings = sentence_transformer.encode(entities)
    print("Embedded :)")

    # Calculate cosine similarities
    similarities = torch.nn.functional.cosine_similarity(torch.tensor(query_embedding), torch.tensor(entity_embeddings))
    print("Got similarities tensor")
    return similarities.tolist()


def get_relevant_entities(query: str, threshold: float = 0.5) -> List[str]:
    """
    Get relevant entities based on semantic similarity to the user query.
    """
    entities = create_graph()
    print("Created graph!")
    similarities = calculate_similarity(query, entities)
    print("Calculated similarity!")
    relevant_entities = [entities[i] for i, sim in enumerate(similarities) if sim > threshold]
    print("Found relevant entities")
    return relevant_entities


__cached_graph = None


def create_graph():
    """
    Loads ontology graph from file.
    """
    global __cached_graph
    try:
        if __cached_graph is None:
            __cached_graph = list(get_ontology(config.ONTOLOGY_FILE).load().classes())
            __cached_graph = [entity.name for entity in __cached_graph]
        return __cached_graph
    except FileNotFoundError:
        print(f"Source file {config.ONTOLOGY_FILE} not found. Retrying in 5 seconds...")
        return None
