import chromadb
from chromadb import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import json
from langchain.embeddings import OpenAIEmbeddings
import core.config as config

# chroma_client = chromadb.HttpClient(host=config.chromadb_uri, port=config.chromadb_port,
#                                     settings=Settings(allow_reset=True, anonymized_telemetry=False))
# embedding_function = OpenAIEmbeddingFunction(api_key=config.openai_api_key)

# chroma's OpenAIEmbeddingFunction limits requests to 3 per min, 
# langchain's OpenAIEmbeddings handles retries.

persist_directory = "chroma"
client = chromadb.PersistentClient(path=persist_directory)
embeddings = OpenAIEmbeddings(openai_api_key=config.openai_api_key)
test_collection_name = "collection_name"
cities_collection_name = "getCities"


def create_embedded_collection(collection_name, file_name):
    coll = client.get_or_create_collection(name=collection_name,
                                    metadata={"hnsw:space": "cosine"},
                                    # embedding_function=embedding_function
                                    )
    file_path='../data/' + file_name
    data = json.load(open(file_path, encoding='utf-8-sig'))
    to_be_embedded_list = []
    for item in data:
        info = item["Description"]
        info = info.split('(')[0].strip().lower()  # 'Абазівка (Полтавський р-н..)' -> 'абазівка', search perf
        to_be_embedded_list.append(info)
    # to_be_embedded_list = to_be_embedded_list[:110]  # demo, first letter 'A'
    # print(len(to_be_embedded_list))
    # print(to_be_embedded_list[:3])
    embeddings_list = embeddings.embed_documents(to_be_embedded_list)
    print(len(embeddings_list[0]))
    print(len(embeddings_list))

    for i in range(len(to_be_embedded_list)):
        coll.add(
            ids=data[i]['Ref'],
            embeddings=embeddings_list[i],
            documents=data[i]['Description'],
            metadatas=data[i]
        )
    print(len(coll.get(include=["documents"])['ids']))

    # return coll.get(include=["documents"])


def query_collection(collection_name, query, n_results=15):
    coll = client.get_collection(name=collection_name)
    query_embedding = embeddings.embed_documents([query.lower()])
    results = coll.query(
        # query_texts=[query.lower()],
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "distances"]
        # include=["documents", "distances", "metadatas"]  # with metadata
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )

    return results


def get_collection(collection_name):
    coll = client.get_collection(name=collection_name)

    return coll.get(include=["documents"])


def demo():
    coll = client.create_collection(name=test_collection_name,
                                           metadata={"hnsw:space": "cosine"})
    # Add docs to the collection. Can also update and delete. Row-based API coming soon!
    coll.add(
        documents=["This is document1", "This is document2"],
        # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
        metadatas=[{"source": "notion"}, {"source": "google-docs"}],  # filter on these!
        ids=["doc1", "doc2"],  # unique for each doc
    )

    # Query/search 2 most similar results. You can also .get by id
    results = coll.query(
        query_texts=["This is a query document"],
        n_results=2
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )

    return results


# print(demo())
print(query_collection(collection_name=cities_collection_name, query="антонівка"))
# print(get_collection(cities_collection_name))
# print(create_embedded_collection(cities_collection_name, "getCities.json"))
