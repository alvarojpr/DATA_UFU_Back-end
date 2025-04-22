from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

@patch("services.obter_transporte_Intercampi.obter_horarios_intercampi")
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

@patch("services.obter_transporte_050.obter_transporte_050")
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




# no terminal, pytest teste.py