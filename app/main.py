from typing import Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from app.auth import verify_api_key
from app.inference import generate_answer

app = FastAPI(title="BFSI GenAI App", version="1.0.0")


class GenerateRequest(BaseModel):
    query: str = Field(..., description="User question")
    context: Optional[str] = Field(default=None, description="Optional external context")


class GenerateResponse(BaseModel):
    model: str
    answer: str
    usage: Optional[dict] = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse, dependencies=[Depends(verify_api_key)])
def generate(request: GenerateRequest) -> dict:
    return generate_answer(request.query, request.context)
