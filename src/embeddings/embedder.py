from langchain_openai import OpenAIEmbeddings

def embed_texts(texts, openai_key):
    """Embed a list of texts using OpenAI embeddings."""
    embedder = OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions=2048,
        openai_api_key=openai_key
    )
    return embedder.embed_documents(texts)
