from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.rag.vectorstore import create_collection
from backend.app.api.chat import router as chat_router
from backend.app.api.upload import router as upload_router
from backend.app.core.cache import get_cache, set_cache

app = FastAPI(
    title="Production RAG Chatbot",
    version="1.0.0"
)

# Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes here

app.include_router(chat_router)
app.include_router(upload_router)
#startup event

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Production RAG backend is running"
    }





#Health check

@app.on_event("startup")
def startup():
    create_collection()