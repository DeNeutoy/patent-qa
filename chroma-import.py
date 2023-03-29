from copy import deepcopy

import openai
import chromadb


openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
    api_key="your key here",
    model_name="text-embedding-ada-002"
)

client = chromadb.Client(chromadb.config.Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/Users/will/Sandbox/chroma"
))

collection = client.create_collection(name="will_test_clean_collection", embedding_function=openai_ef)

def get_metadata_from_scraped_patent(scraped_patent):
    meta_copy = deepcopy(scraped_patent["metadata"])
    if "publication-reference" in meta_copy:
        return {
            "original_id": meta_copy["publication-reference"]["document-id"]["doc-number"],
        }
    return {}

def get_document_from_scraped_patent(scraped_patent):
    abstract = scraped_patent["abstract"]
    description = scraped_patent["description"]
    full_doc = f"abstract | {abstract} | description | {description}"
    # TODO: figure out batching. Biggest one is ~6 times this.
    truncated = full_doc[:25000]
    return truncated

def make_chroma_input_from_scraped_data(scraped_data_list):
    documents = []
    metadatas = []
    ids = []
    for idx, scraped_patent in enumerate(scraped_data_list):
        ids.append(str(idx))
        metadatas.append(get_metadata_from_scraped_patent(scraped_patent))
        documents.append(get_document_from_scraped_patent(scraped_patent))
    return (documents, metadatas, ids)

# Get data in the format shown in the data folder
scraped_patents = []
documents, metadatas, ids = make_chroma_input_from_scraped_data(scraped_patents)

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

just_id_results = collection.query(
    query_texts=["What do you need to make an electromagnetic shield?"],
    n_results=5,
    include=[]
)
winning_patent_id = just_id_results["ids"][0][0]

print(f"ID of most similar patent was {winning_patent_id}")