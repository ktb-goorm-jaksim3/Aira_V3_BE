from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException
from sqlalchemy.orm import Session
from service.chat import generate_text
from service.health import health_check_service
from service.load import load_heavy_service
from service.auth import read_users_me, register, login
from db.database import get_db
from schemas import user_schema
from models.chat import ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

app = FastAPI()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/generate/")
async def generate_text_route(request: ChatRequest):
    return generate_text(request)

@router.get("/me")
async def read_user_me_route(token: str, db: Session = Depends(get_db)):
    return read_users_me(token, db)

@router.post("/auth/register", response_model=user_schema.UserResponse)
async def register_route(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return register(user, db)

@router.post("/auth/login", response_model=user_schema.Token)
async def login_route(request: Request, user: user_schema.UserLogin, db: Session = Depends(get_db)):
    # 요청 바디 전체를 로깅
    body = await request.body()
    print("Raw request body:", body)
    print("Parsed user data:", user.dict())
    return login(user, db)

@router.get("/health")
async def health_check_route():
    return health_check_service()

@router.get("/load")
async def load_heavy_route():
    return load_heavy_service()

@router.get("/auth/me", response_model=user_schema.UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 특정 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)