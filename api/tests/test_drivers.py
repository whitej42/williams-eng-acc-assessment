from fastapi.testclient import TestClient
from ..main import app
from ..routers import drivers

client = TestClient(app)

def test_get_drivers():
    response = client.get("/drivers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Lewis Hamilton"

def test_get_driver():
    response = client.get("/drivers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["driverId"] == 1
    assert data["name"] == "Lewis Hamilton"

def test_get_driver_not_found():
    response = client.get("/drivers/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Driver not found"}