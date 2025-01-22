from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 2000
    temperature: float = 0.7