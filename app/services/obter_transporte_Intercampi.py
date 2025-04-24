import requests
from bs4 import BeautifulSoup
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from app.models.tabela_transporte import Model_Transporte, Model_Pontos, Model_Horarios

import requests
from bs4 import BeautifulSoup

def obter_horarios_intercampi():
    urls = [
        ('https://proae.ufu.br/intercampi?field_campus_origem_tid=511&field_campus_destino_tid=510', 'Boa Vista → Araras'),
        ('https://proae.ufu.br/intercampi?field_campus_origem_tid=510&field_campus_destino_tid=511', 'Araras → Boa Vista')
    ]

    pontos_dict = {}

    for url, rota in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        divs = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-6 col-lg-6')

        horarios = []
        for div in divs:
            hora_div = div.find('div', class_='field-name-field-hora-saida')
            if hora_div:
                for span in hora_div.find_all('span', class_='date-display-single'):
                    hora = span.text.strip()
                    horarios.append(hora)

        if rota not in pontos_dict:
            pontos_dict[rota] = []
        pontos_dict[rota].extend(horarios)

    pontos_e_horarios = []
    for parada, horarios in pontos_dict.items():
        pontos_e_horarios.append({
            "ponto": parada,
            "horarios": horarios
        })

    return {
        "transporte": "intercampi",
        "Pontos_e_horarios": pontos_e_horarios
    }


def salvar_horarios_intercampi_no_bd(db: Session):
    dados = obter_horarios_intercampi()

    transporte = db.query(Model_Transporte).filter_by(nome="intercampi").first()
    if not transporte:
        transporte = Model_Transporte(nome="intercampi")
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

def obter_transporte_Intercampi(db: Session, tipo: str):
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
    transporte = db.query(Model_Transporte).filter_by(nome="intercampi").first()
    if not transporte:
        salvar_horarios_intercampi_no_bd(db)
    return obter_transporte_Intercampi(db, "intercampi")
