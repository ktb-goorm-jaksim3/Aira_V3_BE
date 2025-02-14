import os
import requests
from models.chat import ChatRequest
from fastapi import HTTPException

# GPT Worker의 URL을 환경 변수에서 가져옴
GPT_WORKER_URL = os.getenv("GPT_WORKER_URL", "http://gpt-worker:9000/generate/")

async def generate_text(chat_request: ChatRequest) -> dict:
    try:
        payload = {
            "prompt": chat_request.prompt,
            "max_tokens": chat_request.max_tokens,
            "temperature": chat_request.temperature
        }

        # GPT Worker API 호출
        response = requests.post(GPT_WORKER_URL, json=payload)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"GPT Worker 호출 실패: {response.text}")

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API 호출 실패: {str(e)}")