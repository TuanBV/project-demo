from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_products():
    response = client.get('/product')
    assert response.status_code == 200