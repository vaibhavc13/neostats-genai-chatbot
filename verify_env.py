import os
from dotenv import load_dotenv, find_dotenv

print(f"Current working directory: {os.getcwd()}")
env_path = find_dotenv()
print(f"Found .env at: {env_path}")

loaded = load_dotenv()
print(f"load_dotenv returned: {loaded}")

groq_key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY present: {bool(groq_key)}")
if groq_key:
    print(f"GROQ_API_KEY length: {len(groq_key)}")
    print(f"GROQ_API_KEY prefix: {groq_key[:4]}...")
openai_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY present: {bool(openai_key)}")
