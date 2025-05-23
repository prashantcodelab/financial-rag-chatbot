
# Entry point for ingesting documents and indexing them in Pinecone
from src.utils.config_loader import load_config
from src.ingestion.file_parser import parse_raw_files
from src.ingestion.chunking import smart_chunk_documents
from src.vector_store.pinecone_client import connect_pinecone_and_get_index
from src.embeddings.embedder import embed_texts
import uuid
from tqdm import tqdm

def upsert_chunks(index, chunks, openai_key, batch_size=100):
    """
    Upserts chunks into a Pinecone index.

    Args:
        index (pinecone.Index): The Pinecone index to upsert chunks into.
        chunks (list): A list of chunks to upsert.
        openai_key (str): The OpenAI API key used for embedding.
        batch_size (int, optional): The number of chunks to process in each batch. Defaults to 100.
    """
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i + batch_size]
        texts = [chunk['content'] for chunk in batch]
        embeddings = embed_texts(texts, openai_key)
        vectors = [
            {
                'id': str(uuid.uuid4()),
                'values': vec,
                'metadata': {**chunk['metadata'], 'content': chunk['content']}
            } for chunk, vec in zip(batch, embeddings)
        ]
        index.upsert(vectors=vectors)

if __name__ == '__main__':
    cfg = load_config('config.yaml') #load config
    docs = parse_raw_files('data/RAWDATA/') #parsing documents
    chunks = smart_chunk_documents(docs) # create chunks RecursiveCharacterTextSplitter
    index = connect_pinecone_and_get_index(cfg['pinecone'], cfg['pinecone_index']) # connect to pinecone and get index
    upsert_chunks(index, chunks, cfg['open_ai']) # call upsert chunks