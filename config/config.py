import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# API Keys - It is recommended to set these as environment variables
# or fill them in here for local testing (do not commit keys to git)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Search API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# App Settings
APP_TITLE = "Strategic Business Intelligence Analyst"
APP_ICON = "📊"

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" # Free local model
# EMBEDDING_MODEL = "text-embedding-3-small" # OpenAI model (requires key)
