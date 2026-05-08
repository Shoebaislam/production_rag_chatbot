from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.app.models.schemas import ChatRequest
from backend.app.rag.chain import stream_answer

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat")
async def chat(request: ChatRequest):

    async def event_generator():
        async for chunk in stream_answer(request.question):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )