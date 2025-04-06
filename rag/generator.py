import os

from openai import OpenAI
import config


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from config import GEN_MODEL
from jinja2 import Template


def generate_response(query: str, relevant_entities: list[str], retrieved_docs: list[str], history: list[str]):
    with open(config.SUPPLY_CHAIN_PROMPT_FILE, "r", encoding="utf-8") as f:
        template_text = f.read()

    # format input blocks
    for i, doc in enumerate(retrieved_docs):
        print(doc)
        print()
    context_block = "\n".join([f"{i + 1}. {doc.page_content}" for i, (doc, _) in enumerate(retrieved_docs)])
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
    response = client.chat.completions.create(model=GEN_MODEL,
                                              messages=[
                                                  {"role": "system", "content": "You are a highly skilled Supply Chain "
                                                                                "Assistant specialized in vendor analysis, risk assessment, and market intelligence."},
                                                  {"role": "user", "content": rendered_prompt}
                                              ],
                                              temperature=0.3)
    return response.choices[0].message.content
