import pytest

def test_health_api(client):
    response = client.get("/api/health")
    assert response.status == '200 OK'

def test_availability_api(client):
    response = client.get("/api/availability")
    assert response.status == '200 OK'