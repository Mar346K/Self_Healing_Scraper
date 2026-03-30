### 🕸️ Autonomous Data Refinery (Self-Healing Scraper)

A deterministic, polyglot data ingestion pipeline designed for volatile public web sources.

Standard web scrapers rely on brittle CSS selectors that break the moment a target website updates its UI. This architecture solves the "Day-1" pipeline fragility problem by utilizing an asynchronous, AI-driven self-healing protocol.

## 🏗️ The Architecture

The system prioritizes speed and cost-efficiency using a **Plan-Execute-Verify** loop:
1. **Fast Path ($0 Cost):** The Celery worker checks Redis for cached CSS extraction rules and attempts a high-speed Playwright extraction.
2. **The Healing Path:** If the DOM has mutated and extraction fails, the pipeline routes the raw HTML payload to a Gemini 2.5 Flash microservice.
3. **Deterministic Output:** The LLM is mathematically forced via Google's `google-genai` SDK to extract the requested schema *and* write new Playwright CSS selectors.
4. **System Learning:** The new rules are cached in Redis, allowing subsequent scrapes of that domain to return to the Fast Path.

```mermaid
graph TD
    A[Client Request + JSON Schema] -->|POST /extract| B(FastAPI Gateway)
    B -->|Async Dispatch| C{Redis Queue}
    C --> D[Celery Worker Node]
    D --> E{Cache Check}
    E -->|Rules Found| F[Playwright Fast Extract]
    E -->|No Rules / UI Mutated| G[Playwright Raw DOM Fetch]
    G --> H[Gemini 2.5 Flash Healer]
    H -->|Extracts Data & New Rules| I[(Update Redis Cache)]
    F --> J[Standardized JSON Output]
    H --> J
```

## 🚀 DevSecOps & Enterprise Standards
* Zero-Trust Secrets: API keys managed via pydantic-settings.

* Strict Guardrails: CI/CD pipeline enforces ruff formatting, mypy static typing, and bandit AST security scanning on every commit.

* Bleeding-Edge Inference: Includes experimental support for Google Research's TurboQuant (3-bit KV Cache compression) for local, OOM-resistant HTML processing on consumer hardware.

## 💻 Quick Start (Dockerized)
Spin up the entire microservice cluster locally:

```Bash
docker compose up -d --build
```

# Send a dynamic extraction request:


```Bash
curl -X POST http://localhost:8000/extract \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "target_schema": {"main_heading": "string"}}'
```
