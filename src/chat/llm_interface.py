from langchain_openai import ChatOpenAI

def get_chat_model(api_key):
    """Initialize ChatOpenAI model."""
    return ChatOpenAI(model="gpt-4o", temperature=0.2, openai_api_key=api_key)
