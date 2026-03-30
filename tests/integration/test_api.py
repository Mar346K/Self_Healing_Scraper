from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_extract_endpoint_accepts_payload():
    response = client.post(
        "/extract",
        json={"url": "https://example.com", "target_schema": {"title": "string"}},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    assert "task_id" in response.json()
