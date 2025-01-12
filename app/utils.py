import openai 
from sqlalchemy.orm import Session
import crud
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY 

def perform_translation(task: int, text: str, languages: list, db: Session):
    translations = {}
    for lang in languages:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that translates text into {lang}."},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error: {e}"

    crud.update_translation_task(db, task, translations)



