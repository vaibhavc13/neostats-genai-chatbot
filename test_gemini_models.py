import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)
    
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-1.0-pro",
        "models/gemini-1.5-flash",
        "models/gemini-pro"
    ]    
    print(f"Testing models with API Key: {api_key[:5]}...")
    
    for model_name in models_to_test:
        print(f"\nTesting {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"SUCCESS: {model_name}")
            print(f"Response: {response.text}")
            break # Stop after first success
        except Exception as e:
            print(f"FAILED: {model_name}")
            print(f"Error: {e}")
