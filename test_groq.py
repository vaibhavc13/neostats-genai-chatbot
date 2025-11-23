import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found.")
else:
    print(f"Testing Groq with key: {api_key[:5]}...")
    try:
        chat = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile"
        )
        response = chat.invoke("Hello")
        print("SUCCESS: Groq is working!")
        print(f"Response: {response.content}")
    except Exception as e:
        print("FAILED: Groq")
        print(f"Error: {e}")
