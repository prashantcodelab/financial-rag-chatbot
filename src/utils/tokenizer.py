import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text):
    return len(encoding.encode(text))

def truncate_texts_by_token_limit(texts, max_tokens):
    total = 0
    output = []
    for text in texts:
        tokens = count_tokens(text)
        if total + tokens > max_tokens:
            break
        output.append(text)
        total += tokens
    return output
