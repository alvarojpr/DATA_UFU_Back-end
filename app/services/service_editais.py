from sqlalchemy.orm import Session
from app.models.tabela_editais import Model_Edital
from app.schemas.schema_edital import EditalCreate, EditalUpdate

def get_edital(db: Session, link: str):
    return db.query(Model_Edital).filter(Model_Edital.link == link).first()

def create_edital(db: Session, edital: EditalCreate):
    novo_edital = Model_Edital(**edital.model_dump())
    db.add(novo_edital)
    db.commit()
    db.refresh(novo_edital)
    return novo_edital

def update_edital(db: Session, link: str, edital: EditalUpdate):
    edital_db = get_edital(db, link)
    if not edital_db:
        return None
    for key, value in edital.model_dump(exclude_unset=True).items():
        setattr(edital_db, key, value)
    db.commit()
    db.refresh(edital_db)
    return edital_db

def delete_edital(db: Session, link: str):
    edital_db = get_edital(db, link)
    if not edital_db:
        return None
    db.delete(edital_db)
    db.commit()
    return edital_db
