import os

import nltk
import torch
from collections import deque
from fastapi import APIRouter
from langchain_community.vectorstores import FAISS

import config
from rag.chains.kb import create_graph
from rag.chains.retriever import get_global_retriever
from rag.schemas.models import Question, Answer
from rag.chains.retriever import setup_global_retriever
from langchain.embeddings import HuggingFaceEmbeddings
from rag.chains.kb import get_relevant_entities
from geofeature import GeofeaturesSwagger
from rag.generator import generate_response

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
HISTORY_LEN = 5

nltk.download('punkt_tab')

# FastAPI router initialization
router = APIRouter()
chat_history = deque(maxlen=HISTORY_LEN)
create_graph()

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_index = FAISS.load_local(config.INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
setup_global_retriever(faiss_index)
geofeats_swagger = GeofeaturesSwagger(os.path.join(config.PROJECT_FOLDER_PATH, 'geofeature.csv'))


def answer_query(query: str, history: list[str]):
    relevant_entities = get_relevant_entities(query)
    docs = get_global_retriever().retrieve(query, k=10)
    if len(docs) != 0:
        geospatial_urls = geofeats_swagger.compute_relevant_documents(query)
        geospatial_urls = [g[:-5] for g in geospatial_urls if g.endswith('.json')]
        urls = [doc.metadata['company_url'].split('/')[2] for doc, _ in docs]
        intersection = set(urls).intersection(set(geospatial_urls))
        selected_documents = docs[:5]
        for i in range(5, len(urls)):
            if urls[i] in intersection:
                selected_documents.append(docs[i])
    else:
        selected_documents = []

    response = generate_response(query, relevant_entities, selected_documents, history)
    return response


@router.post("/chat", response_model=Answer)
async def ask_question(question: Question):
    try:
        print(question.userInput)
        context = answer_query(question.userInput, chat_history)
        return Answer(textResponse=context, textExplanation='', data='', label='question')

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
        return Answer(textResponse="Something went wrong, I'm not able to answer your question.", textExplanation="",
                      data="", label="Error")
