import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from backend.app.models.schemas import UploadResponse
from backend.app.rag.ingest import ingest_text_file

router = APIRouter(prefix="/api", tags=["Upload"])

UPLOAD_DIR = "uploads"


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # 👇 Runs in background
    background_tasks.add_task(
        ingest_text_file,
        file_path
    )

    return UploadResponse(
        message="File uploaded successfully. Indexing started in background.",
        filename=file.filename
    )