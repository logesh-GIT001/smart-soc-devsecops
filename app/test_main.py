from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_triage_critical():
    payload = {
        "src_ip": "192.168.1.100",
        "dst_ip": "10.0.0.1",
        "protocol": "TCP",
        "bytes_sent": 100000,
        "packets": 5000,
        "duration": 0.5,
        "flags": "SYN",
    }
    response = client.post("/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "CRITICAL"
    assert "confidence" in data
    assert "explanation" in data


def test_triage_benign():
    payload = {
        "src_ip": "10.0.0.5",
        "dst_ip": "10.0.0.1",
        "protocol": "TCP",
        "bytes_sent": 100,
        "packets": 5,
        "duration": 2.0,
    }
    response = client.post("/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "Benign"


def test_triage_missing_field():
    # Missing required fields — should return 422
    response = client.post("/triage", json={"src_ip": "1.2.3.4"})
    assert response.status_code == 422
