from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.services.obter_editais import obter_editais_db


router_editais = APIRouter()

@router_editais.get("/editais")
def listar_editais(db: Session = Depends(get_db)):
    return obter_editais_db(db)