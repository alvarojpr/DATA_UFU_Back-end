# quando o aluno estiver logado, ele pode adicionar e remover disciplinas. Também pode consulta-las.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.schema_disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse, GradeResponse
from app.models import tabela_AlunoDisciplina
from app.models.tabela_disciplina import Model_Disciplina
from typing import List
from services.obter_disciplinas import salvar_disciplinas_no_bd

disciplina_router = APIRouter()

#############################################################################################################
@disciplina_router.post("/disciplinas/popular_bd")
def popular_banco_com_pdf(db: Session = Depends(get_db)):
    # Verifica se já existem disciplinas cadastradas
    disciplinas_existentes = db.query(Model_Disciplina).first()
    if disciplinas_existentes:
        raise HTTPException(status_code=400, detail="O banco de dados já está populado com disciplinas.")

    try:
        salvar_disciplinas_no_bd(db, pdf_path="resources/horarios.pdf")
        return {"msg": "Disciplinas salvas no banco de dados com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar disciplinas: {str(e)}")
    
# DISCIPLINAS
# o aluno não cria nem atualiza disciplinas. essas rotas é para os desenvolvedores popularem o database.
@disciplina_router.post("/disciplinas/criar", response_model=DisciplinaResponse)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    nova_disciplina = Model_Disciplina(**disciplina.model_dump())
    db.add(nova_disciplina)
    db.commit()
    db.refresh(nova_disciplina)
    return nova_disciplina


@disciplina_router.put("/disciplinas/atualizar/{nome_disciplina}", response_model=DisciplinaResponse)
def atualizar_disciplina(nome_disciplina: str, disciplina: DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina_existente = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    
    # Atualiza os campos fornecidos na requisição
    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(disciplina_existente, key, value)

    db.commit()
    db.refresh(disciplina_existente)

    return disciplina_existente


@disciplina_router.delete("/disciplinas/excluir/{nome_disciplina}")
def excluir_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    db.delete(disciplina)
    db.commit()
    return (f"",disciplina.Model_Disciplina.nome, " Removida.")

#############################################################################################################








#############################################################################################################
# RELACIONAMENTO |ALUNO|~~~~|DISCIPLINA|
@disciplina_router.post("/disciplinas/add/{nome_disciplina}")
def adicionar_disciplina(nome_disciplina: str, aluno_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    # Verifica se já existe essa associação
    associacao_existente = db.query(tabela_AlunoDisciplina).filter_by(aluno_id=aluno_id, disciplina_id=disciplina.id).first()
    if associacao_existente:
        raise HTTPException(status_code=400, detail="Disciplina já adicionada ao aluno")

    nova_associacao = tabela_AlunoDisciplina.insert().values(aluno_id=aluno_id, disciplina_id=disciplina.id)
    db.execute(nova_associacao)
    db.commit()

    return {"msg": "Disciplina adicionada com sucesso"}

# Remover disciplina do aluno
@disciplina_router.delete("/disciplinas/remover/{nome_disciplina}")
def remover_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(tabela_AlunoDisciplina).filter_by(nome_disciplina=nome_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    # Lógica para remover a disciplina do aluno
    return {"msg": "Disciplina removida"}

# Consultar disciplina
@disciplina_router.get("/disciplinas/consultar/{nome_disciplina}", response_model=DisciplinaResponse)
def consultar_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(tabela_AlunoDisciplina).filter_by(nome_disciplina=nome_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

#############################################################################################################



#############################################################################################################
#Retorna a grade horária do aluno autenticado.
@disciplina_router.get("/disciplinas/grade", response_model=List[GradeResponse])
def get_grade(db: Session = Depends(get_db)):
    grade = (
        db.query(Model_Disciplina.nome, Model_Disciplina.dia_semana, Model_Disciplina.horario)
        .all()
    )
    
    if not grade:
        raise HTTPException(status_code=404, detail="Nenhuma disciplina encontrada na grade")
    
    return grade
