import json
from urllib.parse import urlparse
from typing import Any, Dict, cast
import redis

from src.workers.celery_app import celery_app
from src.scrapers.engine import StandardScraper
from src.healers.llm_extractor import AIHealer
from src.core.config import settings

# Connect directly to the local Redis instance to use as our rule cache
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


# Ignore Celery's missing type stubs for this specific decorator
@celery_app.task(name="extract_data_task")  # type: ignore[untyped-decorator]
def extract_data_task(url: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
    print(f"\n[Worker] Processing request for: {url}")

    domain = urlparse(url).netloc
    cache_key = f"extraction_rules:{domain}"

    scraper = StandardScraper(headless=True)

    # 1. Check Redis for cached rules
    cached_rules_str = redis_client.get(cache_key)

    if cached_rules_str:
        print("[Worker] ⚡ Cached CSS rules found! Attempting Fast Extraction...")

        # Cast the Redis return as a string, then cast the JSON output as a Dict
        rules_str = cast(str, cached_rules_str)
        rules = cast(Dict[str, str], json.loads(rules_str))

        try:
            # Try to grab the data using standard Playwright methods
            fast_data = scraper.fast_extract(url, rules)
            print("[Worker] ✅ Fast Extraction Successful! ($0 cost, 0 LLM latency)")
            return {
                "status": "success",
                "method": "fast_cache",
                "url": url,
                "data": fast_data,
            }
        except Exception as e:
            print(f"[Worker] ⚠️ Fast Extraction Failed: {str(e)}")
            print("[Worker] 🚑 Initiating Self-Healing Protocol...")
    else:
        print(
            "[Worker] 🔍 No rules cached for this domain. Initiating AI Extraction..."
        )

    # 2. The Healing Protocol (If cache is empty or UI changed)
    try:
        raw_html = scraper.fetch_html(url)
        print("[Worker] Raw DOM fetched. Handing to AI Healer...")

        # Ask Gemini for the data AND the new rules
        ai_payload = AIHealer.extract_and_learn(raw_html, target_schema)

        extracted_data = ai_payload.get("extracted_data", {})
        new_rules = ai_payload.get("extraction_rules", {})

        # 3. Save the new rules to Redis so we don't have to use the AI next time
        if new_rules:
            redis_client.set(cache_key, json.dumps(new_rules))
            print(f"[Worker] 🧠 System Learned! New rules cached for {domain}.")

        return {
            "status": "success",
            "method": "ai_healed",
            "url": url,
            "data": extracted_data,
            "learned_rules": new_rules,
        }

    except Exception as e:
        print(f"[Worker] ❌ Total Pipeline Failure: {str(e)}")
        return {"status": "failed", "url": url, "error": str(e)}
