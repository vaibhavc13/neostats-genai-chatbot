import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import sys

# Add project root to path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import config

def get_embedding_model(provider="huggingface"):
    """
    Get the embedding model based on the provider.
    
    Args:
        provider (str): 'huggingface', 'openai', or 'google'
        
    Returns:
        Embeddings: The LangChain embeddings model
    """
    try:
        if provider == "huggingface":
            # Uses local model, no API key needed for this specific one usually, 
            # but good to have for consistency.
            return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
            
        elif provider == "openai":
            if not config.OPENAI_API_KEY:
                raise ValueError("OpenAI API Key is missing in config")
            return OpenAIEmbeddings(
                api_key=config.OPENAI_API_KEY,
                model="text-embedding-3-small"
            )
            
        elif provider == "google":
            if not config.GOOGLE_API_KEY:
                raise ValueError("Google API Key is missing in config")
            return GoogleGenerativeAIEmbeddings(
                google_api_key=config.GOOGLE_API_KEY,
                model="models/embedding-001"
            )
            
        else:
            # Fallback to huggingface
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")
