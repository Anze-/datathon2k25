import nltk
import torch
from collections import deque
from fastapi import APIRouter
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

import config
from rag.chains.kb import get_relevant_entities, create_graph
from rag.chains.retriever import get_global_retriever
from rag.schemas.models import Question, Answer
from sentence_transformers import SentenceTransformer
from rag.chains.retriever import setup_global_retriever


from rag.generator import generate_response

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
HISTORY_LEN = 5

# Load environment variables
load_dotenv()
nltk.download('punkt_tab')

# FastAPI router initialization
router = APIRouter()
chat_history = deque(maxlen=HISTORY_LEN)
create_graph()

embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faiss_index = None#FAISS.load_local(config.INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
setup_global_retriever(faiss_index)


def answer_query(query: str, history: list[str]):
    print("Getting relevant entities!")
    relevant_entities = get_relevant_entities(query)
    print("Trying to retrieve!")
    docs = get_global_retriever().retrieve(query, k=3)
    print("Retrieved!!!")
    response = generate_response(query, relevant_entities, docs, history)
    return response


@router.post("/chat", response_model=Answer)
async def ask_question(question: Question):
    try:
        context = answer_query(question.userInput, chat_history)
        return Answer(textResponse=context, textExplanation='', data='', label='question')

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
        return Answer(textResponse="Something went wrong, I'm not able to answer your question.", textExplanation="",
                      data="", label="Error")
