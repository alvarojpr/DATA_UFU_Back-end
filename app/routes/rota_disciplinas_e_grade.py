# quando o aluno estiver logado, ele pode adicionar e remover disciplinas. Também pode consulta-las.

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header, Body
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





@disciplina_router.get("/disciplinas/por-aluno/{matricula}")
def obter_disciplinas_por_aluno(matricula: str, db: Session = Depends(get_db)):
    relacoes = db.query(Model_AlunoDisciplina).filter_by(matricula=matricula).all()
    disciplinas = []
    for relacao in relacoes:
        disciplina = db.query(Model_Disciplina).filter_by(id=relacao.disciplina_id).first()
        if disciplina:
            disciplinas.append({
                "id": disciplina.id,
                "nome": disciplina.nome_disciplina,
                "sala": disciplina.sala,
                "professor": disciplina.nome_prof,
                "dia_semana": disciplina.dia_semana,
                "horario": disciplina.horario
            })
    return disciplinas





#############################################################################################################
# RELACIONAMENTO |ALUNO|~~~~|DISCIPLINA|
from pydantic import BaseModel

class DisciplinasRequest(BaseModel):
    aluno_id: str
    disciplinas_ids: List[int]

@disciplina_router.post("/disciplinas/add")
def adicionar_disciplinas(request: DisciplinasRequest, db: Session = Depends(get_db)):
    for disciplina_id in request.disciplinas_ids:
        disciplina = db.query(Model_Disciplina).filter_by(id=disciplina_id).first()
        if not disciplina:
            raise HTTPException(status_code=404, detail=f"Disciplina com ID {disciplina_id} não encontrada")

        # Verifica se a associação já existe
        associacao_existente = db.query(Model_AlunoDisciplina).filter_by(matricula=request.aluno_id, disciplina_id=disciplina.id).first()
        if associacao_existente:
            continue  # Se a associação já existe, não faz nada e continua para as próximas disciplinas

        # Cria a nova associação com aluno e disciplina
        nova_associacao = Model_AlunoDisciplina(matricula=request.aluno_id, disciplina_id=disciplina.id)
        db.add(nova_associacao)

    db.commit()

    return {"msg": "Disciplinas adicionadas com sucesso"}



@disciplina_router.get("/disciplina/obter")
def listar_disciplinas(db: Session = Depends(get_db)):
    disciplinas = db.query(Model_Disciplina).all()

    # Usando um set para garantir que não haja duplicação, com base no código e nome da disciplina
    disciplinas_unicas = {}
    
    for disciplina in disciplinas:
        nome_disciplina = disciplina.nome_disciplina.split('–', 1)[-1].strip() if '–' in disciplina.nome_disciplina else disciplina.nome_disciplina
        codigo = disciplina.nome_disciplina.split('–', 1)[0].strip() if '–' in disciplina.nome_disciplina else disciplina.nome_disciplina

        # Criando uma chave única com base no código e nome da disciplina
        chave_unica = (codigo, nome_disciplina)
        
        if chave_unica not in disciplinas_unicas:
            disciplinas_unicas[chave_unica] = {
                "id": disciplina.id,
                "nome_disciplina": nome_disciplina,
                "codigo": codigo,
                "sala": disciplina.sala,
                "nome_prof": disciplina.nome_prof,
                "dia_semana": disciplina.dia_semana,
                "horario": disciplina.horario
            }

    return list(disciplinas_unicas.values())


@disciplina_router.post("/disciplinas/remover")
def remover_disciplinas(request: DisciplinasRequest, db: Session = Depends(get_db)):
    for disciplina_id in request.disciplinas_ids:
        relacao = db.query(Model_AlunoDisciplina).filter_by(
            matricula=request.aluno_id,
            disciplina_id=disciplina_id
        ).first()
        if relacao:
            db.delete(relacao)
    db.commit()
    return {"msg": "Disciplinas removidas com sucesso"}


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
