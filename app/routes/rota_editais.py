from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.tabela_editais import Model_Edital
from app.schemas.schema_edital import EditalCreate, EditalUpdate, EditalResponse
from app.services.service_editais import get_edital, create_edital, update_edital, delete_edital

editais_router = APIRouter()  # Instanciando como uma rota do FastAPI


@editais_router.get("/editais", response_model=list[EditalResponse])
def listar_editais(db: Session = Depends(get_db)):
    return db.query(Model_Edital).all()
