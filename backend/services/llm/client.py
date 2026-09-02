
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def llm_rewriter(prompt: str) -> str:
   try:
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt    
    )
       
   except Exception as e:
       print(f"Error occurred while generating LLM rewrite: {e}")
       raise
   content = response.text

   if content is None:
       raise ValueError("LLM returned no content")
   return content

def llm_answer(prompt: str) -> str:
    try:
       response = client.models.generate_content(
           model="gemini-3.5-flash-lite",
           contents=prompt          
       )

       print(f"LLM response: {response}")
       content = response.text

       if content is None:
           raise ValueError("LLM returned no content")
       
    except Exception as e:
       print(f"Error occurred while generating LLM answer: {e}")
       raise
    return content