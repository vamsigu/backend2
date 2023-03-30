from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_patients():
    response = client.get('/patients')
    assert response.status_code == 200

def test_get_patient():
    response = client.get('/patients/1')
    assert response.status_code == 200

def test_patient_login():
    response1 = client.post('/login',json={"username": "vamsi@gmail.com", "password": "Vamsi"})
    assert response1.status_code == 200
    response2 = client.post('/login',json={"username": "gude@gmail.com", "password": "Gude"})
    assert response2.status_code == 404

