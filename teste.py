import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from app.routes.rota_usuario import verify_token

client = TestClient(app)

# Mock do verify_token
def mock_verify_token(token: str = None):
    return {"matricula": "123456", "nome": "Test User"}

app.dependency_overrides[verify_token] = mock_verify_token

# Helper para criar usuário
def criar_usuario_teste():
    client.post("/usuario/criar", json={
        "matricula": "123456",
        "nome": "João",
        "email": "joao@test.com",
        "senha": "123456"
    })

# Helper para criar disciplina
def criar_disciplina_teste():
    client.post("/disciplinas/criar", json={
        "nome_disciplina": "teste",
        "codigo": "TESTE123"
    })

def test_deletar_usuario():
    criar_usuario_teste()
    response = client.delete("/usuario/deletar/123456", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200

def test_atualizar_usuario():
    criar_usuario_teste()
    response = client.put(
        "/usuario/update/123456",
        json={
            "nome": "Novo Nome",
            "email": "novoemail@example.com",
            "senha": "nova_senha"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Novo Nome"
    assert response.json()["email"] == "novoemail@example.com"

@pytest.mark.parametrize("url", [
    "/disciplinas/consultar/teste",
    "/disciplinas/grade",
    "/feedback/consultar/123456",
    "/transporte/municipal",
    "/transporte/intercampi",
    "/editais",
    "/fichas",
])
def test_get_routes(url):
    response = client.get(url)
    assert response.status_code in (200, 404)

@pytest.mark.parametrize("url", [
    "/disciplinas/popular_bd",
])
def test_post_routes_no_body(url):
    response = client.post(url)
    assert response.status_code in (200, 422)

@pytest.mark.parametrize("url, payload", [
    ("/disciplinas/criar", {"nome_disciplina": "Matemática", "codigo": "MAT101"}),
    ("/feedback/dar", {"matricula": "123456", "comentario": "Muito bom!"}),
    ("/usuario/criar", {"nome": "João", "email": "joao@test.com", "senha": "123456"}),
    ("/usuario/login", {"email": "joao@test.com", "senha": "123456"}),
    ("/usuario/recuperar", {"matricula": "123456"}),
])
def test_post_routes_with_body(url, payload):
    response = client.post(url, json=payload)
    assert response.status_code in (200, 201, 422)

@pytest.mark.parametrize("url, payload", [
    ("/disciplinas/atualizar/teste", {"nome_disciplina": "Matemática Atualizada", "codigo": "MAT102"}),
    ("/usuario/update/123456", {"email": "novoemail@test.com"}),
])
def test_put_routes(url, payload):
    headers = {"Authorization": "Bearer fake_token"}
    if "/disciplinas/atualizar" in url:
        criar_disciplina_teste()
    if "/usuario/update" in url:
        criar_usuario_teste()
    response = client.put(url, json=payload, headers=headers)
    assert response.status_code in (200, 401, 422, 404)

@pytest.mark.parametrize("url", [
    "/disciplinas/excluir/teste",
    "/disciplinas/remover/teste",
    "/usuario/deletar/123456",
])
def test_delete_routes(url):
    headers = {"Authorization": "Bearer fake_token"}
    if "disciplinas/excluir" in url or "disciplinas/remover" in url:
        criar_disciplina_teste()
    if "disciplinas/remover" in url:
        headers["aluno_id"] = "123456"  # aluno_id obrigatório no header
    if "usuario/deletar" in url:
        criar_usuario_teste()
    response = client.delete(url, headers=headers)
    assert response.status_code in (200, 401, 404, 422)

def test_adicionar_disciplina():
    criar_disciplina_teste()
    response = client.post("/disciplinas/add/teste?aluno_id=1")
    assert response.status_code in (200, 400, 422, 404)
