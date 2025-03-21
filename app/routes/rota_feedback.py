# O usuário, quando logado, pode enviar feedbacks e ler os que já enviou.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.schemas.schema_feedback import FeedbackCreate, FeedbackResponse
from app.models.tabela_feedback import Model_Feedback

feedback_router = APIRouter()

@feedback_router.post("/feedback/dar", response_model=FeedbackResponse)
def enviar_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    novo_feedback = Model_Feedback(**feedback.model_dump())
    db.add(novo_feedback)
    db.commit()
    db.refresh(novo_feedback)
    return novo_feedback

@feedback_router.get("/feedback/consultar/{matricula}", response_model=List[FeedbackResponse])
def consultar_feedbacks(matricula: str, db: Session = Depends(get_db)):
    feedbacks = db.query(Model_Feedback).filter_by(matricula_aluno=matricula).all()
    if not feedbacks:
        raise HTTPException(status_code=404, detail="Nenhum feedback encontrado para este aluno")
    return feedbacks
