from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers.route import router
from db.database import init_db
import os

# 환경변수 로드
load_dotenv(os.getenv("ENV_FILE",".env"))

# Database 초기화
init_db()

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정 수정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vue.js 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# 기본 엔드포인트 확인용
@app.get("/")
async def root():
    return {"message": "API 서버 실행 중"}
