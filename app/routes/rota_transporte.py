from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.services.obter_transportes import obter_transporte


transporte_router = APIRouter()

@transporte_router.get("/transporte/municipal")
def obter_horarios_050(db: Session = Depends(get_db)):
    return obter_transporte(db, "municipal")


@transporte_router.get("/transporte/intercampi")
def obter_horarios_intercampi(db: Session = Depends(get_db)):
    return obter_transporte(db, "intercampi")

