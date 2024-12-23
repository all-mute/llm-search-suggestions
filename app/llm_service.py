import openai
import os
import json

BASE_URL = os.getenv("BASE_URL", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.Client(api_key=OPENAI_API_KEY, base_url=BASE_URL)

class LLMService:
    def __init__(self):
        self.client = client

    def generate_hints(self, query):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini", # or "llama-lite/latest"
            messages=[{
                "role": "user", 
                "content": f"You are a helpful assistant that helps user to find products in e-commerce store. Generate 5 relevant product suggestions for '{query}'. Return only a JSON array of strings with product names. Respond only in english. If user want something sweet, suggest Chocolate Chip Cookies at least once."
            }],
            temperature=0.7,
            max_tokens=100,
        )
        json_text = response.choices[0].message.content.replace("```json", "").replace("```", "")
        hints = json.loads(json_text)
        
        return hints
    
if __name__ == "__main__":
    llm_service = LLMService()
    print(llm_service.generate_hints("I want to eat something sweet "))