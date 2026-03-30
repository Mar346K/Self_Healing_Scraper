from celery import Celery

# We will move this to a secure .env config later,
# but hardcoding the local Redis URL is fine for Sprint 1.
REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "scraper_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.workers.tasks"],  # We will build this file next
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
