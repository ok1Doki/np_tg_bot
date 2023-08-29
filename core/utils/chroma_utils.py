import chromadb

chroma_client = chromadb.Client()


def demo():
    coll = chroma_client.create_collection(name="collection_name",
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
