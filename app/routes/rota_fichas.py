from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.services.obter_fichas import obter_fichas_com_cache

router_fichas = APIRouter()

@router_fichas.get("/fichas")
def listar_fichas(db: Session = Depends(get_db)):
    return obter_fichas_com_cache(db)
