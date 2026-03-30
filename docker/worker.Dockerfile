FROM python:3.12-slim
WORKDIR /app

# 1. Copy the manifest
COPY pyproject.toml .

# 2. Install the Python packages (this installs the Playwright CLI)
RUN pip install --no-cache-dir .

# 3. Now that Playwright is installed, fetch the OS dependencies and the Chromium browser
RUN playwright install-deps && playwright install chromium

# 4. Copy the core logic
COPY src/ /app/src/

# 5. Boot the worker
CMD ["celery", "-A", "src.workers.celery_app", "worker", "--loglevel=info"]
