# tests/test_health.py
from app import app

def test_index_returns_ok():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"OK" in res.data
