import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('/Users/aditya/Desktop/CODEATHON/.env')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

print("Available models:")
for m in genai.list_models():
    print(m.name)