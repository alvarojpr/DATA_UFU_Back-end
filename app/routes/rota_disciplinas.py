from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.schema_disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse
from app.services.service_disciplinas import get_disciplina, create_disciplina, update_disciplina, delete_disciplina

disciplina_router = APIRouter()

@disciplina_router.post("/disciplinas/", response_model=DisciplinaResponse)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    if get_disciplina(db, disciplina.cod_disciplina):
        raise HTTPException(status_code=400, detail="Disciplina já existe")
    return create_disciplina(db, disciplina)

@disciplina_router.get("/disciplinas/{cod_disciplina}", response_model=DisciplinaResponse)
def consultar_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina = get_disciplina(db, cod_disciplina)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

@disciplina_router.put("/disciplinas/{cod_disciplina}", response_model=DisciplinaResponse)
def atualizar_disciplina(cod_disciplina: str, disciplina: DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina_atualizada = update_disciplina(db, cod_disciplina, disciplina)
    if not disciplina_atualizada:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina_atualizada

@disciplina_router.delete("/disciplinas/{cod_disciplina}")
def excluir_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina_excluida = delete_disciplina(db, cod_disciplina)
    if not disciplina_excluida:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return {"detail": "Disciplina excluída com sucesso"}
