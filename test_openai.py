import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Test message to check OpenAI connection."}
            ]
        )
        print("OpenAI API Test Response:", response)
    except Exception as e:
        print("Error testing OpenAI API:", str(e))

test_openai()
