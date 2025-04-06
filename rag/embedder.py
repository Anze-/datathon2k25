import openai
from config import OPENAI_API_KEY, EMBED_MODEL

openai.api_key = OPENAI_API_KEY


def get_embedding(text: str) -> list:
    response = openai.Embedding.create(
        model=EMBED_MODEL,
        input=text,
    )
    return response["data"][0]["embedding"]
