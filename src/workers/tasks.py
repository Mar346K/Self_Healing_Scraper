import time
from typing import Any, Dict

from src.workers.celery_app import celery_app


@celery_app.task(name="extract_data_task")
def extract_data_task(url: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock task to simulate the extraction process.
    """
    print(f"[Worker] Received extraction request for: {url}")

    # Simulate the time it takes to spin up a headless browser and parse the DOM
    time.sleep(2)

    print(f"[Worker] Extraction complete for: {url}")

    return {
        "status": "success",
        "url": url,
        "extracted_data": {"mock_key": "mock_value_ready_for_sprint_2"},
    }
