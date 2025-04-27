# quando o aluno estiver logado, ele pode adicionar e remover disciplinas. Também pode consulta-las.

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.schema_disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse, GradeResponse
from app.models.tabela_AlunoDisciplina import Model_AlunoDisciplina
from app.models.tabela_disciplina import Model_Disciplina
from typing import List
# from services.obter_disciplinas import salvar_disciplinas_no_bd
from app.services.obter_disciplinas import salvar_disciplinas_no_bd

disciplina_router = APIRouter()

#############################################################################################################

@disciplina_router.post("/disciplinas/popular_bd")
async def popular_banco_com_pdf(pdf: UploadFile = File(...), db: Session = Depends(get_db)):
    # Verifica se já existem disciplinas cadastradas
    disciplinas_existentes = db.query(Model_Disciplina).first()
    if disciplinas_existentes:
        raise HTTPException(status_code=400, detail="O banco de dados já está populado com disciplinas.")

    try:
        # Salvar o arquivo temporariamente ou processar diretamente
        with open("resources/horarios.pdf", "wb") as f:
            f.write(await pdf.read())

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
    
    if not disciplina_existente:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(disciplina_existente, key, value)

    db.commit()
    db.refresh(disciplina_existente)

    return disciplina_existente



@disciplina_router.delete("/disciplinas/excluir/{nome_disciplina}")
def excluir_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()

    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    db.delete(disciplina)
    db.commit()
    return {"msg": f"Disciplina {disciplina.nome_disciplina} removida com sucesso"}

#############################################################################################################








#############################################################################################################
# RELACIONAMENTO |ALUNO|~~~~|DISCIPLINA|
@disciplina_router.post("/disciplinas/add/{nome_disciplina}")
def adicionar_disciplina(nome_disciplina: str, aluno_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    associacao_existente = db.query(Model_AlunoDisciplina).filter_by(matricula=aluno_id, disciplina_id=disciplina.id).first()
    if associacao_existente:
        raise HTTPException(status_code=400, detail="Disciplina já adicionada ao aluno")

    nova_associacao = Model_AlunoDisciplina(matricula=aluno_id, disciplina_id=disciplina.id)
    db.add(nova_associacao)
    db.commit()

    return {"msg": "Disciplina adicionada com sucesso"}


# Remover disciplina do aluno
@disciplina_router.delete("/disciplinas/remover/{nome_disciplina}")
def remover_disciplina(nome_disciplina: str, aluno_id: int = Header(...), db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    relacao = db.query(Model_AlunoDisciplina).filter_by(matricula=aluno_id, disciplina_id=disciplina.id).first()

    if not relacao:
        raise HTTPException(status_code=404, detail="Relação aluno-disciplina não encontrada")

    db.delete(relacao)
    db.commit()

    return {"msg": "Disciplina removida do aluno"}

# Consultar disciplina
@disciplina_router.get("/disciplinas/consultar/{nome_disciplina}", response_model=DisciplinaResponse)
def consultar_disciplina(nome_disciplina: str, db: Session = Depends(get_db)):
    disciplina = db.query(Model_Disciplina).filter_by(nome_disciplina=nome_disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

#############################################################################################################



#############################################################################################################
#Retorna a grade horária do aluno autenticado.
@disciplina_router.get("/disciplinas/grade", response_model=List[GradeResponse])
def get_grade(db: Session = Depends(get_db)):
    grade_raw = db.query(Model_Disciplina.nome_disciplina, Model_Disciplina.dia_semana, Model_Disciplina.horario).all()
    
    if not grade_raw:
        raise HTTPException(status_code=404, detail="Nenhuma disciplina encontrada na grade")
    
    # Montar os objetos GradeResponse
    grade = [
        GradeResponse(
            nome_disciplina=disciplina.nome_disciplina,
            dia_semana=disciplina.dia_semana,
            horario=disciplina.horario
        )
        for disciplina in grade_raw
    ]
    
    return grade
