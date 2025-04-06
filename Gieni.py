print("START")

import os
import json
import torch
import numpy as np
import faiss
from tqdm import tqdm
from uuid import uuid4
import gc

from langchain.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore import InMemoryDocstore
from sentence_transformers import SentenceTransformer

folder_path = "./data/hackathon_data/"
NUM_CHUNKS = 1


def load_document(json_file):
    with open(json_file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {json_file}")
    return []


def document_should_skip(url):
    extensions = [".js", ".css", ".pdf", ".csv", ".doc", ".docx"]
    return any(ext in url for ext in extensions)


def data_get_url(data):
    return data.get('url') or data.get('website_url') or "unknown"


def data_get_id(data):
    return data.get('doc_id', str(uuid4()))


def chunkize(text, k):
    parts = text.split("\n")
    chunks = []
    for i in range(0, len(parts), k):
        chunk = parts[i:i + k]
        chunks.append("\n".join(chunk))
    return chunks


def json_to_documents(file_name):
    data = load_document(os.path.join(folder_path, file_name))
    docs = []
    for i, (url, text) in enumerate(data.get('text_by_page_url', {}).items()):
        if document_should_skip(url):
            continue
        try:
            for chunk_idx, chunk in enumerate(chunkize(text, 20)):
                uuid = f"{data_get_id(data)}_{i}_{chunk_idx}"
                metadata = {"company_url": data_get_url(data), "page_index": i, "chunk_index": chunk_idx, "uid": uuid}
                docs.append(Document(page_content=chunk, metadata=metadata))

        except Exception as e:
            print(f"Error processing {url}: {e}")
    return docs


def embed_documents(texts):
    return model.encode(texts, convert_to_numpy=True)


def convert_chunk(chunk, idx, model):
    print("\nProcessing chunk\n", idx, end='\n\r')
    all_docs = []
    i = 0
    for file_name in tqdm(chunk):
        if i % 50 == 0:
            print(f"Processing file {i}/{len(chunk)}: {file_name}", end='\r')
        documents = json_to_documents(file_name)
        all_docs.extend(documents)
        i += 1
    ids = [doc.metadata["uid"] for doc in all_docs]
    return all_docs, ids
    # texts = [doc.page_content for doc in all_docs]

    # pool = model.start_multi_process_pool()
    # embeddings = model.encode_multi_process(texts, pool, batch_size=32)
    # model.stop_multi_process_pool(pool)
    # embeddings = model.encode(texts)
    # return embeddings


def main():
    # Check for GPU
    #  import pdb; pdb.set_trace()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    model = model.to(device)

    files_in_folder = os.listdir(folder_path)[:10]

    chunk_files = [files_in_folder[i::NUM_CHUNKS] for i in range(NUM_CHUNKS)]

    dim = len(model.encode("Hello world"))
    cpu_index = faiss.IndexFlatL2(dim)
    # cpu_index.add(doc_embeddings_np)

    vector_store = FAISS(
        embedding_function=lambda texts: model.encode(texts, convert_to_numpy=True),
        index=cpu_index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

    for i, chunk_file in enumerate(chunk_files):
        docs, ids = convert_chunk(chunk_file, i, model)
        vector_store.add_documents(documents=docs, ids=ids)
        gc.collect()


    vector_store.save_local("faiss_store_working")
    print("Vector store saved to ./faiss_store")


if __name__ == "__main__":
    main()
