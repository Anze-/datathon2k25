### Tentative implementation of a splitter for the documents
# This code is a work in progress and may not be fully functional.
# In the end, we decided to go for a faster and simpler solution

import json
import os
import pickle
from uuid import uuid4

from langchain_core.documents import Document
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor

from tqdm import tqdm

# splitter = SpacyTextSplitter(pipeline="en_core_web_sm", chunk_size=1000, chunk_overlap=100)
folder_path = "./data/hackathon_data/"


def split_documents(documents: list[Document]):
    """
    Splits documents into chunks.
    Args:
        documents: List of documents to be split.

    Returns:
        List of split documents.
    """
    print("Splitting documents...")
    return splitter.split_documents(documents)


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
    return data.get('url') or "unknown"


def data_get_website_url(data):
    return data.get('website_url') or "unknown"


def data_get_id(data):
    return data.get('doc_id', str(uuid4()))


def json_to_documents(file_name):
    data = load_document(os.path.join(folder_path, file_name))
    docs = []
    for i, (url, text) in enumerate(data.get('text_by_page_url', {}).items()):
        if document_should_skip(url):
            continue
        try:
            uuid = data_get_id(data) + "_" + str(i)
            metadata = {"company_url": data_get_website_url(data), 'url': data_get_url(data), "page_index": i,
                        "uid": uuid}
            if len(text) < 10:
                print(f"Empty text for {url}")
                continue
            docs.append(Document(page_content=text, metadata=metadata))

        except Exception as e:
            print(f"Error processing {url}: {e}")
    return docs


def translate_json(file_name):
    data = load_document(os.path.join(folder_path, file_name))
    d = {"company_url": data_get_website_url(data), 'url': data_get_url(data), "text_by_page_url": {}}
    for i, (url, text) in enumerate(data.get('text_by_page_url', {}).items()):
        if document_should_skip(url):
            continue
        try:
            l = []
            uuid = data_get_id(data) + "_" + str(i)
            d["page_index"] = i,
            d["uid"] = uuid
            a = text.split('\n')
            for j in range(0, len(a), 15):
                l.append(a[j:min(j + 15, len(a))])
            for k, elem in enumerate(l):
                d["text_by_page_url"][f'{url}ù{k}'] = elem

        except Exception as e:
            return f"Error processing {url}: {e}"
    return d


def process_files_parallel(files):
    results = []

    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(translate_json, file): file for file in tqdm(files)}

        for future in as_completed(future_to_file):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing file: {e}")

    return results


def main():
    files = os.listdir(folder_path)
    documents = process_files_parallel(files)

    print("saving split documents...")
    with open("chunked/chunked.json", "w") as file:
        json.dump(documents, file)


if __name__ == '__main__':
    main()
