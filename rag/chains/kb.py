from __future__ import annotations

from datetime import time
from typing import Any, Dict, List, Optional
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts.base import BasePromptTemplate
from owlready2 import get_ontology
from pydantic import Field

import warnings

from sentence_transformers import SentenceTransformer

import config
from rag.chains.retriever import get_global_retriever
import torch

warnings.filterwarnings("ignore")

sentence_transformer = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def calculate_similarity(query: str, entities: List[str]) -> List[float]:
    """Calculate semantic similarity between the user query and RDF entities"""
    query_embedding = sentence_transformer.encode([query])
    entity_embeddings = sentence_transformer.encode(entities)

    # Calculate cosine similarities
    similarities = torch.nn.functional.cosine_similarity(torch.tensor(query_embedding), torch.tensor(entity_embeddings))
    return similarities.tolist()


def get_relevant_entities(query: str, threshold: float = 0.5) -> List[str]:
    """
    Get relevant entities based on semantic similarity to the user query.
    """
    entities = create_graph()
    similarities = calculate_similarity(query, entities)
    relevant_entities = [entities[i] for i, sim in enumerate(similarities) if sim > threshold]
    return relevant_entities


def create_graph():
    """
    Loads ontology graph from file.
    """
    while True:
        try:
            graph = get_ontology(config.ONTOLOGY_FILE).load()
            return graph
        except FileNotFoundError:
            print(f"Source file {config.ONTOLOGY_FILE} not found. Retrying in 5 seconds...")
            time.sleep(5)
