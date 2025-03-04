import openai
from app.core.config import settings
import tiktoken

def chunk_text(text, max_tokens=512):
    """Splits text into smaller chunks while counting actual tokens."""
    if isinstance(text, list):  
        text = " ".join(text)  # Convert list to string

    encoding = tiktoken.encoding_for_model("text-embedding-3-large")
    tokens = encoding.encode(text)
    
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [encoding.decode(chunk) for chunk in chunks]  # Convert tokens back to text

def create_embeddings(text):
    """Generates OpenAI embeddings for given text chunks."""
    
    text_chunks = chunk_text(text, max_tokens=512)  # Ensure text is split properly
    
    response = openai.embeddings.create(
        input=text_chunks,
        model="text-embedding-3-large"
    )
    
    embeddings = [data.embedding for data in response.data]
    return embeddings
