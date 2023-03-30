from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_doctors():
    response = client.get('/doctors')
    assert response.status_code == 200

def test_get_doctor():
    response= client.get('/doctors/1')
    assert response.status_code == 200

def test_doctor_login():
    response1 = client.post('/login',json={"username": "ajay@gmail.com", "password": "Ajay"})
    assert response1.status_code == 200
    response2 = client.post('/login',json={"username": "chitra@gmail.com", "password": "Chitra"})
    assert response2.status_code == 404