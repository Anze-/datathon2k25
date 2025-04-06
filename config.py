""" This script contains the project configuration. """

import os

from dotenv import load_dotenv

load_dotenv()

# PATHS
PROJECT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PROJECT_FOLDER_PATH, 'data')
PROMPTS_PATH = os.path.join(PROJECT_FOLDER_PATH, 'rag', 'prompts')
SUPPLY_CHAIN_PROMPT_FILE = os.path.join(PROMPTS_PATH, 'query.txt')


# ONTOLOGY
ONTOLOGY_FILE = os.path.join(DATASET_PATH, 'SupplyChain.rdf')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-3-small"
GEN_MODEL = "gpt-4o-mini"
INDEX_PATH = os.path.join(PROJECT_FOLDER_PATH, "faiss_store_100")
