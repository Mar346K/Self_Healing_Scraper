FROM python:3.12-slim
WORKDIR /app
# Install system dependencies for headless Chromium
RUN apt-get update && apt-get install -y wget gnupg && \
    playwright install-deps
COPY pyproject.toml .
RUN pip install --no-cache-dir .
RUN playwright install chromium
COPY src/ /app/src/
CMD ["celery", "-A", "src.workers.celery_app", "worker", "--loglevel=info"]
