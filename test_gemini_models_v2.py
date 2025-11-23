import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-1.0-pro",
    "models/gemini-1.5-flash",
    "models/gemini-pro"
]

with open("test_results.txt", "w") as f:
    f.write(f"Testing with key: {api_key[:5]}...\n")
    for model_name in models_to_test:
        f.write(f"Testing {model_name}...\n")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            f.write(f"SUCCESS: {model_name}\n")
            f.write(f"Response: {response.text}\n")
        except Exception as e:
            f.write(f"FAILED: {model_name}\n")
            f.write(f"Error: {e}\n")
        f.write("-" * 20 + "\n")
