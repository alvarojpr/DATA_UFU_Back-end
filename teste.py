import pytest
from fastapi.testclient import TestClient
from main import app
from random import randint

client = TestClient(app)

matricula_teste = str(randint(1000, 9999))


# ---------------------------- USUÁRIO ----------------------------
def test_criar_usuario():
    response = client.post("/usuario/criar", json={
        "matricula": matricula_teste,
        "nome": "Test User",
        "email": f"{matricula_teste}@example.com",
        "senha": "senha123"
    })
    assert response.status_code == 200
    assert response.json()["matricula"] == matricula_teste

def test_login_usuario():
    response = client.post("/usuario/login", json={
        "matricula": matricula_teste,
        "senha": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def obter_token():
    response = client.post("/usuario/login", json={
        "matricula": matricula_teste,
        "senha": "senha123"
    })
    return response.json()["access_token"]


# ---------------------------- DISCIPLINAS ----------------------------
def test_criar_disciplina():
    data = {
        "nome_disciplina": "Matemática",
        "sala": "101",
        "nome_prof": "Prof. Carlos",
        "dia_semana": "Segunda",
        "horario": "08:00"
    }
    response = client.post("/disciplinas/criar", json=data)
    assert response.status_code == 200

def test_consultar_disciplina():
    response = client.get("/disciplinas/consultar/Matemática")
    assert response.status_code == 200
    assert response.json()["nome_disciplina"] == "Matemática"

def test_atualizar_disciplina():
    data = {"sala": "102"}
    response = client.put("/disciplinas/atualizar/Matemática", json=data)
    assert response.status_code == 200
    assert response.json()["sala"] == "102"

def test_excluir_disciplina():
    response = client.delete("/disciplinas/excluir/Matemática")
    assert response.status_code == 200

def test_grade():
    response = client.get("/disciplinas/grade")
    assert response.status_code in [200, 404]  # pode não ter nenhuma disciplina


# ---------------------------- FEEDBACK ----------------------------
def test_enviar_feedback():
    data = {
        "matricula_aluno": matricula_teste,
        "texto": "Muito bom!"
    }
    response = client.post("/feedback/dar", json=data)
    assert response.status_code == 200
    assert response.json()["texto"] == "Muito bom!"

def test_consultar_feedbacks():
    response = client.get(f"/feedback/consultar/{matricula_teste}")
    assert response.status_code in [200, 404]


# ---------------------------- TRANSPORTE ----------------------------
def test_transporte_municipal():
    response = client.get("/transporte/municipal")
    assert response.status_code == 200

def test_transporte_intercampi():
    response = client.get("/transporte/intercampi")
    assert response.status_code == 200


# ---------------------------- EDITAIS ----------------------------
def test_listar_editais():
    response = client.get("/editais")
    assert response.status_code == 200


# ---------------------------- FICHAS ----------------------------
def test_listar_fichas():
    response = client.get("/fichas")
    assert response.status_code == 200


# ---------------------------- USUÁRIO: RECUPERAÇÃO E EXCLUSÃO ----------------------------
def test_atualizar_perfil():
    token = obter_token()
    data = {"nome": "Novo Nome"}
    response = client.put(f"/usuario/update/{matricula_teste}", json=data, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in [200, 404]

def test_excluir_usuario():
    token = obter_token()
    response = client.delete(f"/usuario/deletar/{matricula_teste}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in [200, 404]

def test_recuperar_senha():
    response = client.post("/usuario/recuperar", params={"matricula": matricula_teste})
    assert response.status_code in [200, 404]