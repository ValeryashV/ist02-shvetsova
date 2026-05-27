from mistralai.client import Mistral
import os
import json
from dotenv import load_dotenv
from flask import session
load_dotenv()


# Подключение mistral
def get_ai_answer(user_text, history=None):
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if not api_key:
        return 'Ошибка: ключ API не найден', []
    client = Mistral(api_key=api_key)
    messages = history if history else []
    messages.append({"role": "user", "content": user_text})
    try:
        res = client.chat.complete(
            model='mistral-small-latest',
            messages = messages
        )
        answer = res.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        return answer, messages
    except Exception as e:
        print(f'Mistral Error: {e}')
        return 'ИИ временно недоступен. Попробуйте позже.', messages

