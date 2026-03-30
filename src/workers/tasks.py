from typing import Any, Dict

from src.workers.celery_app import celery_app
from src.scrapers.engine import StandardScraper
from src.healers.llm_extractor import AIHealer


@celery_app.task(name="extract_data_task")
def extract_data_task(url: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
    print(f"[Worker] Spinning up headless browser for: {url}")

    scraper = StandardScraper(headless=True)

    try:
        # 1. Fetch the raw DOM
        raw_html = scraper.fetch_html(url)
        print(f"[Worker] Successfully extracted {len(raw_html)} characters of HTML.")

        # 2. Pass to the AI Healer
        extracted_json = AIHealer.extract_json(raw_html, target_schema)
        print("[Worker] AI Extraction Successful!")

        return {"status": "success", "url": url, "data": extracted_json}

    except Exception as e:
        print(f"[Worker] Pipeline failed: {str(e)}")
        return {"status": "failed", "url": url, "error": str(e)}
