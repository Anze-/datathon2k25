from __future__ import annotations
from typing import Any, Dict, List, Optional
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts.base import BasePromptTemplate
from pydantic import Field

import warnings

from sentence_transformers import SentenceTransformer

from rag.chains.retrieval import get_global_retriever
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


class GraphSparqlQAChain(Chain):
    graph:'typing.Any' = Field(exclude=True)
    sparql_generation_select_chain: LLMChain
    sparql_generation_update_chain: LLMChain
    sparql_intent_chain: LLMChain
    qa_chain: LLMChain
    return_sparql_query: bool = False
    input_key: str = "query"
    output_key: str = "result"
    sparql_query_key: str = "sparql_query"
    allow_dangerous_requests: bool = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.retriever = get_global_retriever()
        if self.allow_dangerous_requests is not True:
            raise ValueError(
                "In order to use this chain, you must acknowledge that it can make dangerous requests."
            )

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def get_entities(self) -> str:
        """Get all entities and individuals from the RDF graph"""
        ontology_entities = [str(cls) for cls in self.graph.classes()]
        ontology_individuals = [str(ind) for ind in self.graph.individuals()]
        return ontology_entities + ontology_individuals

    def _call(self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        prompt = inputs[self.input_key]

        entities = self.get_entities()

        similarities = calculate_similarity(prompt, entities)

        k = 5
        top_k_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:k]
        top_k_entities = [entities[i] for i in top_k_indices]

        # create an augmented query with a predefined string
        augmented_query = f"Based on the ontology, the query matches the following entities/classes: {', '.join(top_k_entities)}. {prompt}"

        # vector search
        retrieved_docs = self.retriever.retrieve(augmented_query, k=10)
        vector_context = "\n".join([doc.page_content for doc, score in retrieved_docs])

        combined_context = f"""
                    Semantically Retrieved Documents:
                    {vector_context}
                    """

        result = self.qa_chain(
            {"prompt": prompt, "context": combined_context, "query": augmented_query},
            callbacks=callbacks,
        )
        res = result[self.qa_chain.output_key]
        chain_result: Dict[str, Any] = {self.output_key: res}
        return chain_result

    @classmethod
    def from_llm(
            cls,
            llm: BaseLanguageModel,
            qa_prompt: BasePromptTemplate,
            sparql_select_prompt: BasePromptTemplate,
            sparql_update_prompt: BasePromptTemplate,
            sparql_intent_prompt: BasePromptTemplate,
            **kwargs: Any,
    ) -> GraphSparqlQAChain:
        qa_chain = LLMChain(llm=llm, prompt=qa_prompt)
        sparql_generation_select_chain = LLMChain(llm=llm, prompt=sparql_select_prompt)
        sparql_generation_update_chain = LLMChain(llm=llm, prompt=sparql_update_prompt)
        sparql_intent_chain = LLMChain(llm=llm, prompt=sparql_intent_prompt)

        return cls(
            qa_chain=qa_chain,
            sparql_generation_select_chain=sparql_generation_select_chain,
            sparql_generation_update_chain=sparql_generation_update_chain,
            sparql_intent_chain=sparql_intent_chain,
            **kwargs,
        )
