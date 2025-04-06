import nltk
import torch
from collections import deque
from fastapi import APIRouter
from dotenv import load_dotenv

from rag.chains.kb import get_relevant_entities
from rag.chains.retriever import get_global_retriever
from rag.schemas.promptmanager import PromptManager
from rag.schemas.models import Question, Answer

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
prompt_manager = PromptManager('prompts/')


def answer_query(query: str, history: list[str]):
    relevant_entities = get_relevant_entities(query)
    docs = get_global_retriever().retrieve(query, k=3)
    response = generate_response(query, relevant_entities, docs, history)
    return response


def prompt_classifier(input: Question):
    """
    Dummy classifier: Replace with your actual logic if needed.
    """
    # Use simple routing for demo
    return 'q'


async def translate_answer(question: Question, question_language: str, context: str):
    """
    Translates the output into user's language using prompt template.
    """
    prompt = prompt_manager.get_prompt('translate').format(
        _CONTEXT_=context,
        _USER_QUERY_=question.userInput,
        _LANGUAGE_=question_language
    )
    print(f"Translating response to {question_language}")
    return generate_response(prompt, [])  # Using same generator


@router.post("/chat", response_model=Answer)
async def ask_question(question: Question):
    try:
        # Translate input to English
        lang_prompt = prompt_manager.get_prompt('get_language').format(
            _USER_QUERY_=question.userInput
        )
        translated_question = generate_response(lang_prompt, [])
        question_language, question.userInput = translated_question.split("-", 1)
        print(f"Detected Language: {question_language} | Translated: {question.userInput}")

        # classify
        label = prompt_classifier(question)

        # mapping of handlers
        handlers = {
            'q': lambda: answer_query(question, chat_history),
        }

        if label not in handlers:
            context = generate_response(question.userInput, [])
            chat_history.append({
                'question': question.userInput,
                'answer': context
            })
            if question_language.lower() != "english":
                context = await translate_answer(question, question_language, context)
            return Answer(textResponse=context, textExplanation='', data='', label='response')

        # Run handler
        context = await handlers[label]()
        if question_language.lower() != "english":
            context = await translate_answer(question, question_language, context)
        chat_history.append({
            'question': question.userInput,
            'answer': context
        })
        return Answer(textResponse=context, textExplanation='', data='', label=label)

    except Exception as e:
        print(f"Error: {e}")
        return Answer(textResponse="Something went wrong, I'm not able to answer your question.", textExplanation="",
                      data="", label="Error")
