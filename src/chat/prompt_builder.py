from src.utils.tokenizer import truncate_texts_by_token_limit

def build_context_prompt(user_query, retrieved_chunks):
    """Construct the prompt with retrieved context for LLM."""
    contexts = [chunk["content"] for chunk in retrieved_chunks]
    trimmed = truncate_texts_by_token_limit(contexts, max_tokens=8000)
    context = "\n---\n".join(trimmed)
    return f"""You are a financial analyst assistant. Use the following context to help answer the user's question.

Context:
{context}

User Question:
{user_query}

If the context contains relevant information, use it to answer the user's question."""
