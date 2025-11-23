import os
import sys
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import config


def get_llm(provider="groq", model_name=None, openai_api_key=None):
    """
    Initialize and return the chat model based on provider.
    
    Args:
        provider (str): 'groq', 'openai', or 'google'
        model_name (str): Optional specific model name
        openai_api_key (str): Optional API key for OpenAI
        
    Returns:
        BaseChatModel: The LangChain chat model
    """
    try:
        if provider == "groq":
            if not config.GROQ_API_KEY:
                raise ValueError("Groq API Key is missing")
            return ChatGroq(
                api_key=config.GROQ_API_KEY,
                model=model_name or "llama-3.3-70b-versatile"
            )
            
        elif provider == "openai":
            api_key = openai_api_key or config.OPENAI_API_KEY
            if not api_key:
                raise ValueError("OpenAI API Key is missing")
            return ChatOpenAI(
                api_key=api_key,
                model=model_name or "gpt-4o-mini"
            )
            
        elif provider == "google":
            if not config.GOOGLE_API_KEY:
                raise ValueError("Google API Key is missing")
            return ChatGoogleGenerativeAI(
                google_api_key=config.GOOGLE_API_KEY,
                model=model_name or "gemini-2.5-flash"
            )
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as e:
        raise RuntimeError(f"Failed to initialize {provider} model: {str(e)}")

# Keep for backward compatibility if needed, but redirect to new function
def get_chatgroq_model():
    return get_llm("groq")