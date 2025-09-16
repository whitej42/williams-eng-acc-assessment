from fastapi.testclient import TestClient
from ..main import app
from ..routers import circuits

client = TestClient(app)

def test_get_circuits():
    response = client.get("/circuits/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["circuit_name"] == "Silverstone"

def test_get_circuit():
    response = client.get("/circuits/1")
    assert response.status_code == 200
    data = response.json()
    assert data["circuitId"] == 1
    assert data["circuit_name"] == "Silverstone"

def test_get_circuit_not_found():
    response = client.get("/circuits/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Circuit not found"}