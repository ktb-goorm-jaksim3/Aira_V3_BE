from models.chat import ChatRequest, ChatResponse
import openai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 클라이언트 생성
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_text(chat_request: ChatRequest) -> ChatResponse:
    try:
        # print(f"📡 OpenAI API 호출: {chat_request}")  # 요청 데이터 출력

        response = client.chat.completions.create(
            model="gpt-4",  # gpt-4 또는 gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # 시스템 메시지
                {"role": "user", "content": chat_request.prompt},               # 사용자 메시지
            ],
            max_tokens=chat_request.max_tokens,
            temperature=chat_request.temperature,
        )

        # 응답 데이터 변환
        response_text = response.choices[0].message.content
        # print(f"✅ OpenAI API 응답: {response_text}")  # 응답 내용 출력

        return ChatResponse(response=response_text)
    except Exception as e:
        # print(f"❌ OpenAI API 호출 실패: {str(e)}")  # 에러 메시지 출력
        raise ValueError(f"OpenAI API 호출 실패: {str(e)}")