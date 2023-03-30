from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_appointments():
    response = client.get('/appointment')
    assert response.status_code == 200

def test_get_appointment():
    response = client.get('/appointment/1')
    assert response.status_code == 200

