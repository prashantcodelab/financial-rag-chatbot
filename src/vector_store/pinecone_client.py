from pinecone import Pinecone

def connect_pinecone_and_get_index(api_key, index_name):
    """Initialize Pinecone client and return index."""
    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)
