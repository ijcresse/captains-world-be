import pytest

def test_it_should_return_200_on_health_call(client):
    response = client.get("/api/health")
    assert response.status == '200 OK'

def test_it_should_return_200_on_availability_call(client):
    response = client.get("/api/availability")
    assert response.status == '200 OK'