from sqlalchemy.orm import Session
from app.models.tabela_disciplina import Model_Disciplina
from app.schemas.schema_disciplina import DisciplinaCreate, DisciplinaUpdate

def get_disciplina(db: Session, cod_disciplina: str):
    return db.query(Model_Disciplina).filter(Model_Disciplina.cod_disciplina == cod_disciplina).first()

def create_disciplina(db: Session, disciplina: DisciplinaCreate):
    nova_disciplina = Model_Disciplina(**disciplina.model_dump())
    db.add(nova_disciplina)
    db.commit()
    db.refresh(nova_disciplina)
    return nova_disciplina

def update_disciplina(db: Session, cod_disciplina: str, disciplina: DisciplinaUpdate):
    disciplina_db = get_disciplina(db, cod_disciplina)
    if not disciplina_db:
        return None
    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(disciplina_db, key, value)
    db.commit()
    db.refresh(disciplina_db)
    return disciplina_db

def delete_disciplina(db: Session, cod_disciplina: str):
    disciplina_db = get_disciplina(db, cod_disciplina)
    if not disciplina_db:
        return None
    db.delete(disciplina_db)
    db.commit()
    return disciplina_db
