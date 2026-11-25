
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

    data = response.json()
    assert data["recebido"] is True
    assert data["codigo"] == codigo
    assert data["sucesso"] is True
    assert data["lexico"]["sucesso"] is True
    assert data["sintatico"]["sucesso"] is True
    assert data["sintatico"]["ast"]["tipo"] == "PROGRAMA"


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


def test_erro_sintatico_retorna_ast_nula():
    response = client.post(
        "/api/analisar",
        json={"codigo": "numero = 10 +"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["lexico"]["sucesso"] is True
    assert data["sintatico"]["sucesso"] is False
    assert data["sintatico"]["ast"] is None
    assert len(data["sintatico"]["erros"]) > 0


def test_erro_lexico_impede_parser():
    response = client.post(
        "/api/analisar",
        json={"codigo": "numero = @ 10"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["lexico"]["sucesso"] is False
    assert data["sintatico"]["sucesso"] is False
    assert data["sintatico"]["ast"] is None
    assert data["sintatico"]["ignorada"] is True


def test_limite_de_tamanho_da_entrada():
    response = client.post(
        "/api/analisar",
        json={"codigo": "x" * 20001},
    )
    assert response.status_code == 422
