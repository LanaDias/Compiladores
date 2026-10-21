from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_hello():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json()["project"] == "CompilaLab"


def test_analisar_codigo_valido():
    codigo = "numero = 10"
    response = client.post(
        "/api/analisar",
        json={"codigo": codigo},
    )

    assert response.status_code == 200
    assert response.json()["recebido"] is True
    assert response.json()["codigo"] == codigo


def test_analisar_codigo_vazio():
    response = client.post(
        "/api/analisar",
        json={"codigo": ""},
    )

    assert response.status_code == 400


def test_analisar_codigo_com_espacos():
    response = client.post(
        "/api/analisar",
        json={"codigo": "   \n  "},
    )

    assert response.status_code == 400


def test_analisar_sem_campo_codigo():
    response = client.post("/api/analisar", json={})
    assert response.status_code == 422