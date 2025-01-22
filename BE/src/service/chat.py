from fastapi import HTTPException
from models.chat import ChatRequest
from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv(os.getenv("ENV_FILE",".env"))

# OpenAI API 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY",".env"),
)

async def generate_text(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return {
            "prompt": request.prompt, 
            "response": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))