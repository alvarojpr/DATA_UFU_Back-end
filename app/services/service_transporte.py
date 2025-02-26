from sqlalchemy.orm import Session
from models import Model_Horarios, Model_Pontos, Model_Transporte

def obter_horarios(db: Session, transporte_nome: str):
    transporte = db.query(Model_Transporte).filter_by(nome=transporte_nome).first()
    if not transporte:
        return {"erro": "Transporte não encontrado"}
    
    pontos = db.query(Model_Pontos).filter_by(transporte_id=transporte.id).all()
    horarios = {}
    
    for ponto in pontos:
        horarios[ponto.ponto] = [h.horario for h in db.query(Model_Horarios).filter_by(ponto_id=ponto.id).all()]
    
    return {"transporte": transporte.nome, "horarios": horarios}
