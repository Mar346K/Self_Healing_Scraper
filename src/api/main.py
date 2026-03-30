from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from src.workers.tasks import extract_data_task

app = FastAPI(
    title="Self-Healing Scraper API",
    description="API for asynchronous, AI-healed web data extraction.",
    version="0.1.0",
)


class ExtractionRequest(BaseModel):
    url: HttpUrl
    target_schema: Dict[str, Any]


@app.post("/extract")
async def trigger_extraction(request: ExtractionRequest) -> Dict[str, Any]:
    # Dispatch the task to the Redis message queue asynchronously
    task = extract_data_task.delay(str(request.url), request.target_schema)

    return {
        "message": "Extraction task accepted.",
        "url": str(request.url),
        "status": "queued",
        "task_id": task.id,
    }
