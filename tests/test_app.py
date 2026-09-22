import os

from app import app


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Production Readiness DevOps Lab" in response.data


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["service"] == "production-readiness-lab"


def test_failure_endpoint_disabled_by_default():
    os.environ.pop("ENABLE_FAILURE_TESTS", None)

    client = app.test_client()

    response = client.get("/test-error")

    assert response.status_code == 403