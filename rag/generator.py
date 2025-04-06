import openai

import config
from config import OPENAI_API_KEY, GEN_MODEL
from jinja2 import Template

openai.api_key = OPENAI_API_KEY


def generate_response(query: str, relevant_entities: list[str], retrieved_docs: list[str], history: list[str]):

    with open(config.SUPPLY_CHAIN_PROMPT_FILE, "r", encoding="utf-8") as f:
        template_text = f.read()

    # format input blocks
    context_block = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(retrieved_docs)])
    entities_block = ", ".join(relevant_entities)
    history_block = "\n".join(history) if history else "None"

    # render prompt
    prompt_template = Template(template_text)
    rendered_prompt = prompt_template.render(
        kb_entities=entities_block,
        retrieved_docs=context_block,
        history=history_block,
        query=query
    )

    # call the model
    response = openai.ChatCompletion.create(
        model=GEN_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for supply chain professionals."},
            {"role": "user", "content": rendered_prompt}
        ],
        temperature=0.3,
    )

    return response["choices"][0]["message"]["content"]
