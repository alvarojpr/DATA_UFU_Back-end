from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# TESTE DE TRANSPORTE
@patch("app.services.obter_transporte_Intercampi.obter_horarios_intercampi")
def test_transporte_intercampi(mock_preview):
    mock_preview.return_value = {
        "transporte": "intercampi",
        "Pontos_e_horarios": [
            {"ponto": "Boa Vista → Araras", "horarios": ["08:00", "10:00"]},
        ],
    }

    response = client.get("/transporte/intercampi")
    assert response.status_code == 200
    assert response.json()["transporte"] == "intercampi"

@patch("app.services.obter_transporte_050.obter_transporte_050")
def test_transporte_050(mock_preview):
    mock_preview.return_value = {
        "transporte": "municipal",
        "Pontos_e_horarios": [
            {"ponto": "Boa Vista → Araras", "horarios": ["08:00", "10:00"]},
        ],
    }

    response = client.get("/transporte/publico")
    assert response.status_code == 200
    assert response.json()["transporte"] == "municipal"
##########################################################################################################



# #TESTES DE DISCIPLINA
# @patch("app.services.obter_disciplinas.salvar_disciplinas_no_bd")
# def test_rotas_disciplinas(mock_preview):
#     mock_preview.return_value  {
#         "nome"
#     }
#     # 1. Tenta popular o banco com PDF
#     response = client.post("/disciplinas/popular_bd")
#     assert response.status_code in [200, 400]  # Pode já estar populado

#     # 2. Cria uma nova disciplina
#     nova_disciplina = {
#         "nome_disciplina": "Testes Automatizados",
#         "codigo": "TST123",
#         "professor": "Dr. Testador",
#         "horario": "Segunda 10:00-12:00"
#     }
#     response = client.post("/disciplinas/criar", json=nova_disciplina)
#     assert response.status_code == 200
#     assert response.json()["nome_disciplina"] == "Testes Automatizados"

#     # 3. Atualiza a disciplina
#     atualizacao = {
#         "professor": "Dr. Testador Atualizado",
#         "horario": "Segunda 14:00-16:00"
#     }
#     response = client.put("/disciplinas/atualizar", json=atualizacao)
#     assert response.status_code == 200
#     assert response.json()["professor"] == "Dr. Testador Atualizado"

#     # 4. Deleta a disciplina
#     response = client.delete("/disciplinas/excluir")
#     assert response.status_code == 200 or response.status_code == 204
##########################################################################################################



# no terminal, pytest teste.py