# quando o aluno estiver logado, ele pode adicionar e remover disciplinas. Também pode consulta-las.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.schema_disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse, GradeResponse
from app.models import tabela_AlunoDisciplina
from app.models.tabela_disciplina import Model_Disciplina, Dias_da_Semana
from typing import List

disciplina_router = APIRouter()

#############################################################################################################
# DISCIPLINAS
# o aluno não cria nem atualiza disciplinas. essas rotas é para os desenvolvedores popularem o database.
@disciplina_router.post("/disciplinas/criar", response_model=DisciplinaResponse)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    
    return

@disciplina_router.put("/disciplinas/atualizar/{cod_disciplina}", response_model=DisciplinaResponse)
def atualizar_disciplina(cod_disciplina: str, disciplina: DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina_existente = db.query(Model_Disciplina).filter_by(cod_disciplina=cod_disciplina).first()
    
    # Atualiza os campos fornecidos na requisição
    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(disciplina_existente, key, value)

    db.commit()
    db.refresh(disciplina_existente)

    return disciplina_existente


@disciplina_router.delete("/disciplinas/excluir/{cod_disciplina}")
def excluir_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(cod_disciplina=cod_disciplina).first()
    db.delete(disciplina)
    db.commit()
    return (f"",disciplina.Model_Disciplina.nome, " Removida.")

#############################################################################################################








#############################################################################################################
# RELACIONAMENTO |ALUNO|~~~~|DISCIPLINA|
@disciplina_router.post("/disciplinas/add/{cod_disciplina}")
def adicionar_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(tabela_AlunoDisciplina).filter_by(cod_disciplina=cod_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    # Lógica para associar a disciplina ao aluno
    return {"msg": "Disciplina adicionada"}

# Remover disciplina do aluno
@disciplina_router.delete("/disciplinas/remover/{cod_disciplina}")
def remover_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(tabela_AlunoDisciplina).filter_by(cod_disciplina=cod_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    # Lógica para remover a disciplina do aluno
    return {"msg": "Disciplina removida"}

# Consultar disciplina
@disciplina_router.get("/disciplinas/consultar/{cod_disciplina}", response_model=DisciplinaResponse)
def consultar_disciplina(cod_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(tabela_AlunoDisciplina).filter_by(cod_disciplina=cod_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

#############################################################################################################



#############################################################################################################
#Retorna a grade horária do aluno autenticado.
@disciplina_router.get("/disciplinas/grade", response_model=List[GradeResponse])
def get_grade(db: Session = Depends(get_db)):
    grade = (
        db.query(Model_Disciplina.nome, Dias_da_Semana.dia, Dias_da_Semana.horario)
        .join(Dias_da_Semana, Model_Disciplina.cod_disciplina == Dias_da_Semana.cod_disciplina)
        .all()
    )
    
    if not grade:
        raise HTTPException(status_code=404, detail="Nenhuma disciplina encontrada na grade")
    
    return grade
