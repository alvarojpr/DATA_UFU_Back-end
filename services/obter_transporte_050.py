import requests
from bs4 import BeautifulSoup
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from app.models.tabela_transporte import Model_Transporte, Model_Pontos, Model_Horarios

def obter_horarios_municipal():
    url = 'https://www.montecarmelo.mg.gov.br/transporte-publico'
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    titulos = soup.find_all('div', class_='linha50')

    pontos_dict = {}
    for titulo in titulos:
        linhas = titulo.text.strip().splitlines()
        for linha in linhas:
            linha = linha.strip()
            if '»' in linha:
                horario, parada = linha.split(' » ', 1)
                parada = parada.strip()
                horario = horario.strip()
                if parada not in pontos_dict:
                    pontos_dict[parada] = []
                pontos_dict[parada].append(horario)

    pontos_e_horarios = []
    for parada, horarios in pontos_dict.items():
        pontos_e_horarios.append({
            "ponto": parada,
            "horarios": horarios
        })

    return {
        "transporte": "municipal",
        "Pontos_e_horarios": pontos_e_horarios
    }

def salvar_horarios_municipal_no_bd(db: Session):
    dados = obter_horarios_municipal()

    transporte = db.query(Model_Transporte).filter_by(nome="municipal").first()
    if not transporte:
        transporte = Model_Transporte(nome="municipal")
        db.add(transporte)
        db.commit()
        db.refresh(transporte)

    for ponto_data in dados["Pontos_e_horarios"]:
        ponto = db.query(Model_Pontos).filter_by(ponto=ponto_data["ponto"], transporte_id=transporte.id).first()
        if not ponto:
            ponto = Model_Pontos(ponto=ponto_data["ponto"], transporte_id=transporte.id)
            db.add(ponto)
            db.commit()
            db.refresh(ponto)

        for horario in ponto_data["horarios"]:
            horario_existente = db.query(Model_Horarios).filter_by(horario=horario, ponto_id=ponto.id).first()
            if not horario_existente:
                novo_horario = Model_Horarios(horario=horario, ponto_id=ponto.id)
                db.add(novo_horario)

    db.commit()

def obter_transporte_municipal(db: Session, tipo: str):
    transporte = db.query(Model_Transporte).filter_by(nome=tipo).first()
    if not transporte:
        return {"detail": "Tipo de transporte não encontrado"}

    resultado = []
    for ponto in transporte.pontos:
        horarios = [h.horario for h in ponto.horarios]
        resultado.append({
            "ponto": ponto.ponto,
            "horarios": horarios
        })

    return {
        "transporte": transporte.nome,
        "Pontos_e_horarios": resultado
    }

# 🔄 Esta função executa o ciclo completo: verifica, popula, retorna
def preview_intercampi_com_cache(db: Session = Depends(get_db)):
    transporte = db.query(Model_Transporte).filter_by(nome="municipal").first()
    if not transporte:
        salvar_horarios_municipal_no_bd(db)
    return obter_transporte_municipal(db, "municipal")