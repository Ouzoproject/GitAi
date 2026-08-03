from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("LLM_API_KEY"),
)

def llm(prompt: str) -> str:
   response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )
   content = response.choices[0].message.content

   if content is None:
       raise ValueError("LLM returned no content")
   return content