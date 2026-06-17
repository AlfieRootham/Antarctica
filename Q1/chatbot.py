import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

#load the path to the . env fils so that the api key can be found
env_path = Path(__file__).resolve().parent.parent / ".env"

#print("Current working directory:", Path.cwd())
#print("Env path:", env_path)
#print("Env exists:", env_path.exists())
#print("raw values:", dotenv_values(env_path))



load_dotenv(env_path)
api = os.getenv("GEMINI_API_KEY")
#print(api)
if not api:
    raise ValueError("GEMINI_API_KEY not found. Create a .env file using .env.example.")

client = genai.Client(api_key=api)

def gemini(user_message):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
    )
    return response.text
'''
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
'''