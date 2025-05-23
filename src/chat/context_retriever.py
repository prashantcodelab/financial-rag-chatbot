def retrieve_context(query, index, embedder, k=8):
    """Retrieve top-k context chunks from Pinecone index based on the query."""
    query_vec = embedder.embed_query(query)
    results = index.query(vector=query_vec, top_k=k, include_metadata=True)
    return [{"content": m["metadata"].get("content", ""), "source": m["metadata"].get("file_name", "unknown")} for m in results["matches"]]
