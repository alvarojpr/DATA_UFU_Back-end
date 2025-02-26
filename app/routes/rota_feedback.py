from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import services, schemas

feedback_router = APIRouter()


@feedback_router.post("/feedback", response_model=schemas.FeedbackResponse)
def enviar_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return services.criar_feedback(db, feedback)


@feedback_router.get("/feedback", response_model=List[schemas.FeedbackResponse])
def consultar_feedbacks(db: Session = Depends(get_db)):
    return services.listar_feedbacks(db)
