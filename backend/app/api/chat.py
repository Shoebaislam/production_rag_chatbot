from fastapi import APIRouter
from backend.app.models.schemas import ChatRequest, ChatResponse
from backend.app.rag.chain import generate_answer

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = generate_answer(request.question)

    return ChatResponse(answer=answer)