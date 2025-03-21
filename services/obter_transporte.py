from sqlalchemy.orm import Session
from app.models.tabela_transporte import Model_Transporte

def obter_horarios(db: Session, tipo: str):
    transporte = db.query(Model_Transporte).filter_by(nome=tipo).first()
    if not transporte:
        return {"detail": "Tipo de transporte não encontrado"}
    
    horarios_e_pontos = []
    for ponto in transporte.pontos:
        horarios_e_pontos.append({
            "ponto": ponto.ponto,
            "horarios": [h.horario for h in ponto.horarios]
        })
    
    return {"transporte": tipo, "Pontos_e_horarios": horarios_e_pontos}