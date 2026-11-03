def test_health_returns_service_status(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Model 2 RAG System"
    assert response.headers["X-Request-ID"]


def test_health_preserves_client_request_id(client):
    response = client.get("/api/health", headers={"X-Request-ID": "test-request"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request"
