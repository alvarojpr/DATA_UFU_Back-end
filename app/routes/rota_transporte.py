from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.obter_transporte_050 import preview_050_com_cache
from services.obter_transporte_Intercampi import preview_intercampi_com_cache


transporte_router = APIRouter()

@transporte_router.get("/transporte/publico")
def obter_horarios_050(db: Session = Depends(get_db)):
    return preview_050_com_cache(db)

@transporte_router.get("/transporte/publico/preview")
def preview_050(db: Session = Depends(get_db)):
    return preview_050_com_cache(db)

@transporte_router.get("/transporte/intercampi")
def obter_horarios_intercampi(db: Session = Depends(get_db)):
    return preview_intercampi_com_cache(db)

@transporte_router.get("/transporte/intercampi/preview")
def preview_intercampi(db: Session = Depends(get_db)):
    return preview_intercampi_com_cache(db)