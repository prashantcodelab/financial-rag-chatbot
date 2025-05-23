from langchain.text_splitter import RecursiveCharacterTextSplitter

def smart_chunk_documents(docs, max_lines=10):
    """Split documents into chunks for processing."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    chunks = []
    for doc in docs:
        content, meta = doc["content"], doc["metadata"]
        if meta.get("file_type") == "excel_sheet":
            lines = content.splitlines()
            for i in range(0, len(lines), max_lines):
                chunk_text = "\n".join(lines[i:i + max_lines])
                chunks.append({"content": chunk_text, "metadata": {**meta, "chunk_index": i // max_lines}})
        else:
            for i, chunk in enumerate(splitter.split_text(content)):
                chunks.append({"content": chunk, "metadata": {**meta, "chunk_index": i}})
    return chunks
