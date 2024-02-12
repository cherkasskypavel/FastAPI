from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_3_posts():
    response = client.get('/posts?limit=10')
    assert response.status_code == 200
    