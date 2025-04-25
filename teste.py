from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# pytest teste.py

########### DE TRANSPORTE ###########
# intercampi da ufu
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

# transporte público municipal
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



########### TESTES DE DISCIPLINAS ##########
# salvar no bd
@patch("app.services.obter_disciplinas.salvar_disciplinas_no_bd")
def test_rotas_disciplinas_salvar(mock_preview):
    # Simula banco já populado com disciplinas
    with patch("app.routes.rota_disciplinas_e_grade.get_db") as mock_get_db:
        mock_db = mock_get_db.return_value

        response = client.post("/disciplinas/popular_bd")

        if(mock_db.query.return_value.first.return_value is None):
            assert response.status_code == 200
            assert response.json()["msg"] == "Disciplinas salvas no banco de dados com sucesso."
        else: # mock_db.query.return_value.first.return_value = True
            assert response.status_code == 400
            assert response.json()["detail"] == "O banco de dados já está populado com disciplinas."
    
#########################################################################################################




########### TESTES DE EDITAIS ##########
# salvar no bd
@patch("app.services.obter_editais.salvar_editais_no_bd")
def test_rotas_editais_salvar(mock_preview):
    with patch("app.routes.rota_editais.get_db") as mock_get_db:
        mock_db = mock_get_db.return_value

        response = client.post("/editais")

        if(mock_db.query.return_value.first.return_value is None): # banco de dados está vazio
            assert response.status_code == 200
        else: # mock_db.query.return_value.first.return_value = True # banco de dados está cheio
            assert response.status_code == 405

    
#########################################################################################################



    

    response = client.get("/transporte/intercampi")
########### TESTES DE FEEDBACK ##########
# enviar feedback
@patch("app.routes.rota_feedback.get_db")  # Mock do banco de dados
@patch("app.routes.rota_feedback.enviar_feedback")  # Mock da função de envio de feedback
def test_rotas_feedback(mock_enviar_feedback, mock_get_db):
    mock_db = mock_get_db.return_value  # Banco mockado
    # Simula um feedback que o mock deve retornar
    mock_preview = {
        "matricula_aluno": "4321",  # Agora matricula_aluno é uma string
        "texto": "feedback qualquer dado por qualquer um é apenas um teste"
    }

    # Mock da função enviar_feedback para retornar uma resposta esperada
    mock_enviar_feedback.return_value = mock_preview  # O que o mock de enviar_feedback retornará
    
    # Criação do client para testar a API
    client = TestClient(app)
    
    # Fazendo a requisição POST para o endpoint de feedback
    response = client.post("/feedback/dar", json=mock_preview)
    
    # Verificando se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert response.json()["matricula_aluno"] == mock_preview["matricula_aluno"]
    assert response.json()["texto"] == mock_preview["texto"]

    
#########################################################################################################